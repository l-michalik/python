# scripts/

Skrypty pomocnicze, nie część pakietu.

- `seed.py` (T13) — generuje N ofert z tagami do bazy. Musi umieć zrobić
  100 000+ rekordów w rozsądnym czasie, bo pomiar N+1 na tysiącu wierszy nic
  nie mówi: planer bazy wybiera tam inny plan niż na milionie.
- `bench.py` (T11) — uruchamia pełną macierz pomiarów i wypisuje tabelę
  gotową do wklejenia do `docs/pomiary/`.
