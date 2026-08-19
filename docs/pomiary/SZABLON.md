# Pomiar: <co mierzone> — T<nr>

**Data:** RRRR-MM-DD
**Maszyna:** procesor / liczba rdzeni fizycznych i logicznych / RAM / system
**Interpreter:** `python -VV` (wklej pełny wynik — wariant free-threading widać właśnie tu)
**Wersje:** biblioteki istotne dla pomiaru, z wersjami z `uv.lock`

## Pytanie

Jedno zdanie. Pomiar bez pytania jest zbiorem liczb, nie wynikiem.

> Przykład: czy zrównoleglenie `normalize_many` skróci czas przetworzenia
> dobowej porcji 4,2 mln ofert poniżej okna nocnego?

## Metoda

- Wejście: rozmiar, charakterystyka, skąd pochodzi (dane produkcyjne czy syntetyczne).
- Sposób pomiaru: `perf_counter` / `process_time` / `cProfile` / licznik zapytań.
- Liczba powtórzeń i który odczyt raportowany (najlepszy / mediana).
- Co zostało wyłączone na czas pomiaru (odśmiecacz, inne procesy, cache).

## Wynik

| wariant | workers | wall_s | cpu_s | cpu/wall | przyspieszenie |
| --- | ---: | ---: | ---: | ---: | ---: |
| sekwencyjnie | 1 | | | | 1,00× |
| wątki | 4 | | | | |
| wątki | 8 | | | | |
| procesy | 4 | | | | |
| asyncio | 8 | | | | |

## Odczyt

Co te liczby rozstrzygają. Konkretnie: która kolumna i dlaczego.

- `cpu/wall ≈ 1` przy N wykonawcach → równoległości nie ma (podpis GIL-a).
- `cpu/wall ≈ N` → praca faktycznie idzie na N rdzeniach.
- `cpu/wall << 1` → obciążenie zdominowane czekaniem.

## Czego to NIE dowodzi

Obowiązkowa sekcja. Co najmniej dwa punkty.

> Przykład: wynik pochodzi z laptopa o 8 rdzeniach; serwer ma 4, więc próg
> opłacalności procesów będzie tam inny. Pomiar nie obejmuje kosztu pamięci
> osobnych interpreterów.

## Decyzja

Jedno zdanie: co robimy i jaka liczba to uzasadnia. Jeśli decyzja brzmi
„zostawiamy sekwencyjnie" — to też jest wynik, i to najczęstszy.
