---
id: pyt-reg-003
title: asyncio — pętla zdarzeń i jej blokowanie
dependsOn: pyt-jun-007, pyt-jun-004
updated: 2026-08-14
---

## Polecenie

Wykryj wywołanie blokujące pętlę zdarzeń i pokaż, po jakim sygnale je rozpoznajesz.

## Odpowiedź

Pętla zdarzeń jest jednym wątkiem, więc każda operacja, która nie oddaje sterowania w `await`, zatrzymuje wszystkie pozostałe zadania na czas swojego trwania. Rozpoznaje się to po objawie: opóźnienia rosną wszystkim żądaniom naraz, proporcjonalnie do obciążenia, a nie tylko temu, które robi coś kosztownego. Potwierdza to tryb diagnostyczny asyncio, który loguje ostrzeżenie za każdą operacją trzymającą pętlę dłużej niż ustalony próg.

## Definicja

Pętla zdarzeń to wątek wykonujący kolejkę zadań i przełączający się między nimi wyłącznie w punktach oznaczonych `await`. Korutyna to funkcja zadeklarowana jako `async def`, która po wywołaniu nie wykonuje się, tylko zwraca obiekt do zaplanowania. Wywołanie blokujące to takie, które oddaje sterowanie dopiero po zakończeniu pracy — synchroniczne zapytanie do bazy, odczyt pliku, pętla licząca.

## Zastosowanie

Bierze się to w usługach obsługujących wiele równoczesnych połączeń, gdzie koszt stosu na wątek zaczyna się liczyć, i wszędzie tam, gdzie framework webowy jest asynchroniczny. comm1t wymaga budowania „scalable, robust backend systems" na stosie z FastAPI, ARQ i Celery, Shelf „concurrency, failure handling, data consistency, async work, and service boundaries", CloudFerro „asynchronicznych metod komunikacji (rpc, kolejki)".

## Jak to działa

Pętla trzyma listę gotowych zadań i selektor systemowy z deskryptorami, na które czeka. Bierze pierwsze gotowe zadanie i wykonuje jego kod aż do `await` — wtedy zadanie deklaruje, na co czeka, i wraca do pętli, która bierze następne. Jeżeli kod między dwoma `await` trwa 300 ms, przez te 300 ms nie wykona się nic innego, łącznie z obsługą nowych połączeń. Tryb diagnostyczny (`asyncio.run(main(), debug=True)` albo zmienna `PYTHONASYNCIODEBUG`) mierzy czas każdego takiego odcinka i loguje ostrzeżenie po przekroczeniu progu `slow_callback_duration`, domyślnie 100 ms. Wyjściem dla kodu blokującego jest `asyncio.to_thread`, który wypycha go do puli wątków — wtedy pętla oddaje sterowanie normalnie.

## Przykład

```python
import asyncio, time

async def obsluz(zadanie_id: int) -> None:
    time.sleep(0.3)                      # blokuje całą pętlę
    # await asyncio.to_thread(time.sleep, 0.3)   # nie blokuje

async def main() -> None:
    await asyncio.gather(*(obsluz(i) for i in range(10)))

asyncio.run(main(), debug=True)
```

Wersja z `time.sleep` kończy się po około 3,0 s i przy każdym zadaniu wypisuje ostrzeżenie o wywołaniu trwającym 0,3 s. Wersja z `to_thread` kończy się po około 0,3 s i nie wypisuje nic. Ten sam błąd w usłudze produkcyjnej daje p95 rosnące liniowo z liczbą równoczesnych żądań, mimo że każde z osobna jest tanie.

## Ograniczenia

Tryb diagnostyczny ma własny narzut i nie włącza się go na produkcji na stałe. Wykrywa odcinki dłuższe niż próg, więc nie pokaże wielu drobnych blokad sumujących się do tego samego skutku. Sama zamiana kodu na `async` niczego nie przyspiesza, jeśli biblioteka pod spodem jest synchroniczna — sterownik bazy musi być asynchroniczny, inaczej `await` tylko zmienia składnię. Wypchnięcie pracy do puli wątków rozwiązuje blokowanie pętli, ale nie omija GIL-a przy pracy liczącej.

## Alternatywy

Pula wątków zamiast pętli — gdy równoczesnych operacji są setki, a nie tysiące, i nie chce się przepisywać całego stosu na `async`. Osobny proces roboczy i kolejka zadań — gdy operacja trwa sekundy i nie ma powodu trzymać na nią połączenia HTTP. Uruchomienie kilku procesów usługi za load balancerem — gdy usługa jest już asynchroniczna, ale jeden rdzeń przestaje wystarczać. Kryterium: `asyncio`, gdy dominują równoczesne operacje sieciowe i cały stos ma asynchroniczne sterowniki.

## Typowe błędy

- Wywołanie synchronicznego klienta HTTP albo sterownika bazy wewnątrz `async def` — najczęstsza przyczyna „asynchronicznej" usługi wolniejszej od synchronicznej.
- Wywołanie korutyny bez `await`, przez co zwraca obiekt, nikt jej nie planuje, a program działa dalej, jakby wszystko się udało.
- `asyncio.gather` bez ograniczenia równoległości, wypuszczający dziesięć tysięcy żądań naraz w API z limitem stu.
- Pętla licząca w korutynie, wypchnięta potem do `to_thread` i uznana za zrównolegloną — GIL zostaje.
- Tworzenie zadań bez trzymania referencji, przez co odśmiecacz może je usunąć przed zakończeniem.

## Pytania kontrolne

- pytanie: Po przepisaniu usługi na `async` p95 wzrosło zamiast spaść. Jaka jest pierwsza hipoteza i czym ją potwierdzisz?
- odpowiedź: Że pod spodem został synchroniczny sterownik albo klient HTTP, więc każde żądanie trzyma jedyny wątek pętli i opóźnienia sumują się wszystkim naraz. Potwierdzam, uruchamiając z trybem diagnostycznym asyncio i szukając ostrzeżeń o wywołaniach przekraczających `slow_callback_duration` — wskażą one konkretną funkcję; brak ostrzeżeń przy równoczesnym wzroście p95 przesuwa hipotezę na wyczerpaną pulę połączeń.
- pytanie: Skąd wiesz, że `asyncio.to_thread` rozwiązało problem, a nie tylko go przesunęło?
- odpowiedź: Z dwóch pomiarów naraz: czas ścienny całości spada z sumy odcinków do najdłuższego z nich, a ostrzeżenia o wolnych wywołaniach znikają z logu trybu diagnostycznego. Jeśli czas ścienny nie spadł, praca była liczeniem, a nie oczekiwaniem — wtedy pula wątków tylko zdjęła blokadę z pętli, a GIL nadal szereguje wykonanie i problem został przesunięty, nie usunięty.
- pytanie: Dlaczego jedno synchroniczne zapytanie do bazy w `async def` spowalnia także inne żądania?
- odpowiedź: Pętla zdarzeń wykonuje kod jednego zadania aż do `await`; blokujące wywołanie nie oddaje jej sterowania, więc opóźnienie rozlewa się na wszystkie żądania.

## Źródła

- [Developing with asyncio](https://docs.python.org/3/library/asyncio-dev.html) — Python Software Foundation
- [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html) — Python Software Foundation
- [concurrent.futures — Launching parallel tasks](https://docs.python.org/3/library/concurrent.futures.html) — Python Software Foundation
