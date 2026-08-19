---
id: pyt-jun-007
title: Współbieżność z gotowych klocków
dependsOn: pyt-nic-005, pyt-nic-001
updated: 2026-08-14
---

## Polecenie

Wybierz mechanizm współbieżności dla zadania i uzasadnij wybór jego kosztem uruchomienia oraz sposobem przekazywania danych.

## Odpowiedź

Do wielu równoczesnych operacji wejścia-wyjścia bierze się pulę wątków (`ThreadPoolExecutor`) albo pętlę asynchroniczną (`asyncio`); wątki są prostsze, bo nie wymagają przepisania kodu na `async`, pętla jest tańsza przy tysiącach równoczesnych połączeń. Do pracy obciążającej procesor bierze się procesy (`ProcessPoolExecutor`), bo każdy ma własny interpreter i własny GIL, kosztem serializacji danych między nimi. Do pracy, która ma przeżyć restart usługi i być ponawiana, bierze się kolejkę zadań (Celery z RabbitMQ).

## Definicja

Wątek to niezależny ciąg wykonania w tym samym procesie, dzielący z resztą pamięć. Proces ma własną przestrzeń adresową, więc dane trzeba między nimi serializować. Pętla zdarzeń to pojedynczy wątek przełączający się między zadaniami w punktach oczekiwania, oznaczonych słowem `await`. Kolejka zadań to broker przechowujący zlecenia, z którego odrębni pracownicy pobierają je i wykonują poza procesem obsługującym żądanie.

## Zastosowanie

Bierze się to, gdy sekwencyjne wykonanie przestaje mieścić się w czasie odpowiedzi albo gdy operacja trwa dłużej, niż klient jest gotów czekać. CloudFerro wymaga pracy „z kodem wielowątkowym, wieloprocesowym", Fabrity „aplikacji wielowątkowych wykorzystujących bibliotekę Celery, opartych na systemach kolejkowych (RabbitMQ)", a Shelf wymienia „concurrency, failure handling, async work" jednym tchem — bo w praktyce dochodzą razem.

## Jak to działa

Pula wątków trzyma ustaloną liczbę wątków i rozdziela im zadania z kolejki; wątek czekający na sieć zwalnia GIL, więc reszta pracuje. Pula procesów uruchamia osobne interpretery i przesyła do nich argumenty przez serializację — dlatego funkcja i jej argumenty muszą dać się serializować, a koszt przesłania dużego obiektu potrafi przewyższyć zysk z równoległości. Pętla zdarzeń nie ma wątków: wykonuje jedno zadanie, aż to natrafi na `await`, wtedy odkłada je i bierze następne. Kolejka zadań rozdziela wykonanie na dwa procesy: producent zapisuje zlecenie do brokera i natychmiast odpowiada klientowi, pracownik pobiera je i wykonuje, a wynik odkłada osobno.

## Przykład

Pobranie dwudziestu adresów, każdy odpowiada po około 200 ms:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as pula:
    wyniki = list(pula.map(pobierz, adresy))
```

Sekwencyjnie to około 4 s. Przy ośmiu wątkach zadania idą trzema turami, czyli około 600 ms. Podniesienie `max_workers` do 20 zbije to do jednej tury i około 200 ms — ale każdy wątek to własny stos i własne połączenie, więc granicę wyznacza tu limit połączeń po drugiej stronie, a nie liczba rdzeni. Ta sama pula dla funkcji liczącej nie da żadnego przyspieszenia.

## Ograniczenia

Wątki dzielą pamięć, więc każdy współdzielony obiekt mutowalny wymaga synchronizacji; błąd tej klasy nie odtwarza się na żądanie i nie widać go w testach. Procesy nie mają tego problemu, ale płacą sekundami za uruchomienie i serializacją każdego argumentu. Pętla zdarzeń załamuje się od jednego wywołania blokującego — synchroniczne zapytanie do bazy w funkcji `async` zatrzymuje wszystkie zadania naraz. Kolejka zadań wprowadza własną infrastrukturę i pytanie, co zrobić z zadaniem, które padło w połowie.

## Alternatywy

`asyncio` zamiast wątków — gdy równoczesnych połączeń są tysiące i koszt stosu na wątek zaczyna się liczyć. Interpreter bez GIL-a (PEP 779, oficjalnie wspierany od Pythona 3.14) zamiast procesów — gdy dane są duże i serializacja dominuje; wymaga jednak, żeby zależności natywne były w nim bezpieczne. Wypchnięcie pętli do biblioteki natywnej zamiast zrównoleglania — gdy operacja da się wyrazić na całej tablicy. Harmonogram systemowy zamiast Celery — gdy zadanie jest jedno na dobę.

## Typowe błędy

- Dobranie puli procesów do zadania czekającego na sieć — płacisz uruchomieniem i serializacją za coś, co wątki załatwiają za darmo.
- Wywołanie funkcji blokującej wewnątrz `async def`, przez co cała pętla staje na czas tego wywołania.
- Ustawienie liczby wątków „na oko" bez sprawdzenia limitu połączeń bazy albo limitu żądań zewnętrznego API — dławik przesuwa się w miejsce, którego nie kontrolujesz.
- Współdzielenie sesji ORM albo klienta HTTP między wątkami bez sprawdzenia, czy jest do tego przystosowany.
- Zadanie w kolejce bez ustawionego limitu czasu i strategii ponowienia — jedno zawieszone zlecenie blokuje pracownika na stałe.

## Pytania kontrolne

- pytanie: Zadanie sekwencyjne trwa 4 s i składa się z dwudziestu wywołań zewnętrznego API po 200 ms. Ile wątków ustawiasz w puli i czym ograniczysz tę liczbę od góry?
- odpowiedź: Skoro cały czas to oczekiwanie, liczba wątków wprost dzieli czas — dwadzieścia wątków daje jedną turę i około 200 ms. Górną granicę wyznacza nie liczba rdzeni, tylko druga strona: limit równoczesnych żądań tego API oraz pula połączeń, przez którą idą. Ustawiam pulę poniżej niższego z tych limitów, bo przekroczenie zamienia przyspieszenie w odrzucone żądania.
- pytanie: Kolega przepisał funkcję liczącą sumy kontrolne na cztery wątki i czas nie spadł. Co mu odpowiadasz i co proponujesz sprawdzić?
- odpowiedź: To zadanie obciąża procesor, a bajtkod Pythona wykonuje w danej chwili jeden wątek, więc cztery wątki dzielą jeden rdzeń zamiast obsadzić cztery — GIL nie jest tu zwalniany, bo nie ma oczekiwania. Proponuję pulę procesów i zmierzenie, ile kosztuje serializacja danych wejściowych: jeśli przesyłany blok jest duży, zysk z równoległości może zniknąć w koszcie przekazania.
- pytanie: Kiedy zamiast puli wykonawców wybierzesz kolejkę zadań?
- odpowiedź: Gdy praca ma przeżyć restart usługi i być ponawiana, bo broker zapisuje zlecenie poza procesem obsługującym żądanie; pula wykonawców nie daje tej trwałości.

## Źródła

- [concurrent.futures — Launching parallel tasks](https://docs.python.org/3/library/concurrent.futures.html) — Python Software Foundation
- [multiprocessing — Process-based parallelism](https://docs.python.org/3/library/multiprocessing.html) — Python Software Foundation
- [Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html) — Celery
