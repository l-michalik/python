---
id: pyt-reg-001
title: GIL i free-threading — co naprawdę się zrównolegla
dependsOn: pyt-jun-007, pyt-jun-001
updated: 2026-08-14
---

## Polecenie

Zmierz, ile z twojego kodu faktycznie wykonuje się równolegle, i rozstrzygnij na tej podstawie, czy warto sięgać po interpreter bez GIL-a.

## Odpowiedź

Pomiar polega na porównaniu czasu ściennego z czasem procesora dla tego samego obciążenia przy jednym i przy N wątkach. Kod czekający na wejście-wyjście da czas ścienny malejący z liczbą wątków przy prawie stałym czasie procesora; kod liczący da czas ścienny stały, a czas procesora rosnący o narzut przełączeń. Interpreter bez GIL-a warto rozważyć dopiero, gdy pomiar pokazuje drugi przypadek, dane są za duże na serializację do procesów, a wszystkie zależności natywne deklarują zgodność.

## Definicja

GIL to muteks wewnątrz CPythona gwarantujący, że bajtkod wykonuje jeden wątek naraz. Free-threading to wariant kompilacji CPythona bez tej blokady, wprowadzony w 3.13 (PEP 703) i podniesiony do statusu oficjalnie wspieranego w 3.14 (PEP 779) — nadal jako osobny wariant, nie jako domyślne wydanie. Czas ścienny to czas, który upłynął; czas procesora to suma czasu przepracowanego przez wszystkie rdzenie.

## Zastosowanie

To jest pomiar, który rozstrzyga spór „przepisujemy na Go czy nie" liczbą zamiast przekonaniem. EPAM wymaga projektowania „considering NFRs around high throughput and low latency for data processing", Shelf „performance tuning for real-time and high throughput scenarios", a TSS „identyfikowania wąskich gardeł". Wszystkie trzy zaczynają się od odpowiedzi, czy dołożenie równoległości w ogóle ma szansę pomóc.

## Jak to działa

Wątek trzymający GIL oddaje go w dwóch sytuacjach: gdy wchodzi w operację wejścia-wyjścia lub wywołanie natywne deklarujące zwolnienie blokady, i gdy minie interwał przełączania (domyślnie 5 ms, do odczytania przez `sys.getswitchinterval`). Przy pracy liczącej działa wyłącznie druga ścieżka, więc wątki nie liczą równolegle, tylko na zmianę — a każde przełączenie kosztuje. Stąd charakterystyczny objaw: przy czterech wątkach liczących czas ścienny bywa nie tylko taki sam, ale nieco gorszy niż przy jednym. W wariancie bez GIL-a wątki liczą naprawdę równolegle, ale interpreter płaci za to inaczej: liczniki odwołań muszą być bezpieczne wątkowo, więc kod jednowątkowy jest w tym wariancie wolniejszy — i to również jest liczba do zmierzenia, a nie do założenia.

## Przykład

```python
import time, os
from concurrent.futures import ThreadPoolExecutor

def zmierz(funkcja, n_watkow):
    scienny, cpu = time.perf_counter(), time.process_time()
    with ThreadPoolExecutor(max_workers=n_watkow) as pula:
        list(pula.map(funkcja, range(n_watkow)))
    return time.perf_counter() - scienny, time.process_time() - cpu
```

Dla funkcji liczącej sumę kontrolną 200 MB odczyt wygląda typowo tak: 1 wątek — 3,1 s ściennie i 3,1 s procesora; 4 wątki — 3,3 s ściennie i 3,3 s procesora. Stosunek czasu procesora do ściennego bliski jedynce przy czterech wątkach jest dowodem, że równoległości nie ma. Dla funkcji pobierającej dane po sieci ten sam pomiar da 4,0 s / 0,1 s przy jednym wątku i 1,0 s / 0,1 s przy czterech — czas procesora się nie zmienia, bo cały zysk pochodzi z nakładania oczekiwania.

## Ograniczenia

Pomiar czasu procesora nie rozdziela pracy własnej od pracy bibliotek natywnych, które GIL zwalniają — kod wołający NumPy pokaże równoległość, mimo że pętla w Pythonie jej nie ma. Wynik zależy od maszyny, więc liczby z laptopa nie przenoszą się na serwer o innej liczbie rdzeni. Sam stosunek czasów nie mówi, gdzie leży wąskie gardło, tylko czy równoległość działa; do wskazania miejsca potrzebny jest profil. Free-threading nie jest przełącznikiem: wymaga osobnego wariantu interpretera i zależności zbudowanych pod niego.

## Alternatywy

Pula procesów — gdy pomiar potwierdza pracę procesora, a dane wejściowe są małe względem czasu liczenia; kosztem jest serializacja i pamięć na osobne interpretery. Wypchnięcie pętli do warstwy natywnej (NumPy, Polars, rozszerzenie w Rust) — gdy operacja da się wyrazić na całej tablicy; zwykle daje więcej niż zrównoleglenie tej samej pętli. Osobna usługa w innym języku — gdy liczenie jest całą treścią komponentu. `concurrent.interpreters` — gdy izolacja ma być w procesie, a nie między procesami.

## Typowe błędy

- Mierzenie samym czasem ściennym, bez czasu procesora — nie widać wtedy różnicy między „równolegle" a „na zmianę".
- Pomiar na obciążeniu zabawkowym, które mieści się w pamięci podręcznej procesora, i przeniesienie wniosku na dane produkcyjne.
- Uznanie przyspieszenia u kogoś, kto wołał bibliotekę natywną, za dowód, że GIL nie przeszkadza w czystym Pythonie.
- Włączenie wariantu bez GIL-a bez zmierzenia kosztu jednowątkowego — usługa obsługująca głównie wejście-wyjście może na tym stracić.

## Pytania kontrolne

- pytanie: Zwiększyłeś liczbę wątków z 1 do 4 i czas ścienny spadł z 4,0 s do 1,05 s, a czas procesora został na 0,1 s. Co ten wynik dowodzi i czego nie dowodzi?
- odpowiedź: Dowodzi, że obciążenie jest zdominowane oczekiwaniem — czas procesora się nie zmienił, więc zysk pochodzi z nakładania okresów bezczynności, a nie z równoległego liczenia. Nie dowodzi, że skalowanie pójdzie dalej: przy większej liczbie wątków granicę postawi limit połączeń po drugiej stronie, a nie interpreter, więc kolejny pomiar trzeba zrobić na docelowej liczbie równoczesnych żądań.
- pytanie: Czym uzasadnisz przed zespołem decyzję o przejściu na interpreter bez GIL-a i jaką liczbę pokażesz jako koszt tej zmiany?
- odpowiedź: Uzasadnieniem jest pomiar, w którym przy N wątkach czas ścienny nie maleje, a stosunek czasu procesora do ściennego zostaje przy jedynce — czyli praca jest liczeniem, którego GIL nie przepuszcza równolegle. Kosztem, który pokazuję obok, jest czas tego samego obciążenia jednowątkowo w obu wariantach interpretera: wariant bez GIL-a płaci za bezpieczne liczniki odwołań i bywa wolniejszy, więc zysk trzeba przedstawić jako różnicę, a nie samą liczbę rdzeni.
- pytanie: Dlaczego wynik z kodem używającym NumPy nie wystarcza do oceny równoległości własnego bajtkodu?
- odpowiedź: Biblioteka natywna może zwalniać GIL, więc pomiar pokaże równoległość mimo że pętla Pythona jej nie ma; trzeba odseparować koszt biblioteki od własnego kodu lub potwierdzić wynik profilem.

## Źródła

- [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html) — Python Software Foundation
- [PEP 703 — Making the Global Interpreter Lock Optional in CPython](https://peps.python.org/pep-0703/) — Python Software Foundation
- [PEP 779 — Criteria for supported status for free-threaded Python](https://peps.python.org/pep-0779/) — Python Software Foundation
