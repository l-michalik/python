---
id: pyt-reg-005
title: Pomiar wartości zestawu testów
dependsOn: pyt-jun-003, pyt-jun-002
updated: 2026-08-14
---

## Polecenie

Oceń, czy zestaw testów faktycznie chroni przed regresją, i podaj metrykę, na której opierasz tę ocenę.

## Odpowiedź

Pokrycie linii mówi, które linie zostały wykonane, a nie czy cokolwiek zostało sprawdzone — test bez asercji podnosi je tak samo jak dobry. Pokrycie gałęzi jest ostrzejsze, bo wymaga wejścia w obie strony każdego warunku. Twardym pomiarem jest testowanie mutacyjne: narzędzie wprowadza drobne zmiany w kodzie i sprawdza, ile z nich zestaw wykrył. Odsetek zabitych mutantów jest jedyną z tych liczb, która mierzy zdolność wykrywania, a nie samo wykonanie.

## Definicja

Pokrycie linii to udział wykonanych linii w liczbie linii wykonywalnych. Pokrycie gałęzi liczy przejścia przez każdą krawędź warunku, więc `if` bez gałęzi fałszywej jest pokryty tylko w połowie. Mutant to wersja programu z jedną celową zmianą (`>` na `>=`, `+` na `-`, usunięta linia). Mutant zabity to taki, przy którym co najmniej jeden test padł; mutant ocalały wskazuje zachowanie, którego nikt nie sprawdza.

## Zastosowanie

Bierze się to, gdy zestaw testów rośnie, a mimo to regresje trafiają na produkcję — wtedy pytanie „czy mamy dość testów" trzeba zamienić na liczbę. Osiem ogłoszeń w próbce wymaga testów i jakości kodu: CloudFerro „testów jednostkowych zgodnie z TDD", EPAM „automated functional testing and CI/CD pipelines", DCG „automated tests, preferably with pytest", TSS „dbania o jakość, czytelność i wydajność kodu oraz udziału w przeglądach technicznych".

## Jak to działa

Narzędzie pokrycia rejestruje wykonanie przez mechanizm śledzenia interpretera i zapisuje, które linie i krawędzie zostały odwiedzone; tryb gałęziowy włącza się osobno, bo kosztuje więcej. Testowanie mutacyjne działa inaczej: generuje warianty programu i uruchamia na każdym zestaw testów, więc koszt to liczba mutantów razy czas zestawu — dlatego uruchamia się je na wybranym module, a nie na całym repozytorium. Trzeci pomiar, którego nie daje żadne z tych narzędzi, to regresja wydajności: dokłada się ją jako test porównujący czas albo liczbę zapytań z zapisanym punktem odniesienia, żeby zmiana rzędu kosztu padała w potoku, a nie na produkcji.

## Przykład

```python
def rabat(kwota: float, procent: int) -> float:
    if procent > 90:
        procent = 90
    return kwota * (100 - procent) / 100
```

Test na `(100, 50)` daje 100% pokrycia linii i 50% pokrycia gałęzi — warunek nigdy nie był prawdziwy. Mutant zamieniający `> 90` na `>= 90` przeżyje nawet po dołożeniu testu na `(100, 95)`, bo obie wersje obcinają do 90. Zabija go dopiero przypadek `(100, 90)`, który rozstrzyga, po której stronie leży granica. Typowy odczyt na takim module: pokrycie linii 100%, pokrycie gałęzi 78%, mutanty zabite 61% — i to ta trzecia liczba mówi, ile zestaw jest wart.

## Ograniczenia

Pokrycie ma sufit, którego nie warto gonić: ostatnie procenty zwykle dotyczą obsługi błędów niemożliwych do wywołania w teście, a dążenie do stu produkuje testy pisane pod metrykę. Testowanie mutacyjne jest kosztowne czasowo i generuje mutanty równoważne — zmiany, które nie zmieniają zachowania, więc żaden test nie może ich zabić, a raport liczy je jako braki. Żadna z tych metryk nie mówi nic o poprawności specyfikacji: zestaw może w stu procentach sprawdzać zachowanie, które jest błędne.

## Alternatywy

Testy własnościowe (Hypothesis) — gdy braki wskazane przez mutanty leżą w przestrzeni wejść, której nikt nie wymyśli ręcznie. Testy integracyjne na prawdziwej bazie — gdy ocalałe mutanty siedzą w warstwie zapytań, której testy jednostkowe nie dotykają. Przegląd kodu jako pomiar uzupełniający — wychwytuje błędy specyfikacji, na które żadna metryka nie odpowiada. Kryterium: pokrycie gałęzi jako tani wskaźnik ciągły w CI, mutacje punktowo na module krytycznym.

## Typowe błędy

- Ustawienie progu pokrycia linii w CI i uznanie sprawy za zamkniętą — próg spełnia się też testami bez asercji.
- Mierzenie pokrycia bez trybu gałęziowego, przez co warunki bez gałęzi fałszywej wyglądają na sprawdzone.
- Uruchamianie testowania mutacyjnego na całym repozytorium przy każdym scaleniu i wyłączenie go po tygodniu z powodu czasu.
- Traktowanie ocalałych mutantów jako listy zadań bez odsiania równoważnych.
- Brak testu regresji wydajności, przez co zmiana z dwóch zapytań na dwieście przechodzi przegląd, bo testy poprawności są zielone.

## Pytania kontrolne

- pytanie: Moduł ma 100% pokrycia linii, a w zeszłym miesiącu wyszły z niego dwie regresje. Jaką liczbą zastąpisz to pokrycie i co ona pokaże?
- odpowiedź: Odsetkiem zabitych mutantów, uzupełnionym pokryciem gałęzi. Pokrycie linii mierzy wykonanie, nie sprawdzenie, więc test bez asercji podnosi je tak samo jak dobry; mutacje mierzą wprost, ile celowo wprowadzonych zmian zachowania zestaw wykrył. Ocalałe mutanty wskażą przy okazji konkretne linie, w których warunek nie jest sprawdzany po obu stronach granicy.
- pytanie: Dlaczego test na `(100, 95)` nie wystarcza do sprawdzenia obcięcia rabatu do 90 i który przypadek dokładasz?
- odpowiedź: Bo dla 95 zarówno `> 90`, jak i `>= 90` dają ten sam wynik, więc mutant przestawiający granicę przeżywa — test wykonuje linię, ale nie rozstrzyga, po której stronie leży próg. Dokładam przypadek dokładnie na granicy, `(100, 90)`: przy `>= 90` wynik jest ten sam, ale przy przesunięciu granicy o jeden w drugą stronę różnica staje się widoczna i mutant ginie.
- pytanie: Dlaczego wysoki wynik mutacyjny nie potwierdza, że wymagania produktu są właściwe?
- odpowiedź: Mutacje mierzą, czy testy wykrywają zmianę istniejącego zachowania, nie czy to zachowanie spełnia właściwą specyfikację; zestaw może świetnie chronić błędnie zdefiniowaną regułę.

## Źródła

- [Coverage.py](https://coverage.readthedocs.io/en/latest/) — Ned Batchelder
- [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html) — pytest
- [pytest — PyPI](https://pypi.org/project/pytest/) — Python Package Index
