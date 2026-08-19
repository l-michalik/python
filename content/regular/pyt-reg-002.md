---
id: pyt-reg-002
title: Profilowanie czasu i pamięci
dependsOn: pyt-jun-001, pyt-jun-007
updated: 2026-08-14
---

## Polecenie

Wskaż wąskie gardło w wolnym skrypcie i pokaż liczbę przed zmianą oraz po niej.

## Odpowiedź

Najpierw profil deterministyczny (`cProfile`) na całym uruchomieniu — daje ranking funkcji po czasie skumulowanym i mówi, gdzie w ogóle patrzeć. Potem `timeit` na wyizolowanym fragmencie, żeby porównać warianty bez szumu. Do pamięci `tracemalloc`, który zestawia migawki i pokazuje, które linie alokują najwięcej. Zmiana jest udowodniona dopiero wtedy, gdy masz obie liczby zmierzone tym samym sposobem na tym samym wejściu.

## Definicja

Profiler deterministyczny rejestruje każde wejście do funkcji i wyjście z niej, licząc czas własny (spędzony w niej) i skumulowany (razem z wywołaniami wewnątrz). `timeit` uruchamia fragment wielokrotnie i podaje najlepszy wynik z serii, żeby odciąć wpływ innych procesów. `tracemalloc` śledzi alokacje pamięci z przypisaniem do linii kodu i pozwala odjąć od siebie dwie migawki.

## Zastosowanie

Bierze się to, gdy pojawia się zdanie „to jest wolne" — bo bez profilu jest to hipoteza, a poprawki na hipotezę zwykle trafiają w kod, który zajmuje 3% czasu. TSS wymaga „identyfikowania wąskich gardeł oraz wdrażania usprawnień", Fabrity „optymalizacji wydajności aplikacji oraz zapytań do baz danych", Shelf „performance tuning", CloudFerro pisania „wydajnego kodu". Wymóg w tej czy innej formie wystąpił w siedmiu ogłoszeniach na trzynaście.

## Jak to działa

`cProfile` podpina się pod mechanizm śledzenia interpretera, więc każde wywołanie funkcji przechodzi przez dodatkowy kod — narzut jest realny i nierównomierny: uderza mocniej w kod z wieloma drobnymi wywołaniami niż w jedną długą pętlę. Dlatego profil służy do wskazania miejsca, a nie do podawania bezwzględnego czasu. Kolumna czasu skumulowanego pokazuje, ile kosztowało poddrzewo wywołań, więc na jej szczycie zawsze stoi funkcja główna; szuka się pierwszej pozycji, w której czas własny jest duży. `timeit` domyślnie wyłącza odśmiecacz na czas pomiaru i powtarza serię, bo pojedynczy przebieg mierzy głównie stan pamięci podręcznej. `tracemalloc` zapamiętuje przy każdej alokacji ścieżkę wywołań, więc sam kosztuje pamięć i czas — włącza się go na czas diagnozy, nie na stałe.

## Przykład

```python
import cProfile, pstats

cProfile.run("przetworz(dane)", "profil.out")
pstats.Stats("profil.out").sort_stats("tottime").print_stats(10)
```

Typowy odczyt z takiego profilu: `czysc_tekst` — 12,4 s czasu własnego przy 1 200 000 wywołań, `zapisz` — 0,8 s. To jest podstawa do zmiany: kompilacja wyrażenia regularnego raz zamiast w każdym wywołaniu zbija `czysc_tekst` do 2,1 s, czyli całość z 13,4 s do 3,1 s. Bez profilu naturalnym odruchem byłoby optymalizowanie zapisu do bazy, który odpowiada za 6% czasu — nawet doskonała poprawka tam daje najwyżej 0,8 s.

## Ograniczenia

Profil deterministyczny zniekształca proporcje w kodzie o dużej liczbie krótkich wywołań i nie nadaje się do uruchomienia na produkcji pod ruchem — tam potrzebny jest profiler próbkujący. Nie pokazuje czasu spędzonego poza Pythonem: oczekiwanie na bazę widać jako jedną wolną funkcję, bez informacji, które zapytanie i dlaczego. Pomiar na danych testowych bywa myślący za ciebie: wąskie gardło przy dziesięciu tysiącach rekordów bywa gdzie indziej niż przy dziesięciu milionach. `tracemalloc` pokazuje alokacje Pythona, nie pamięć zajętą przez rozszerzenia natywne.

## Alternatywy

Profiler próbkujący (py-spy, `sys.monitoring`) — gdy trzeba zajrzeć do działającego procesu bez jego zatrzymywania i bez narzutu na każde wywołanie. Pomiar czasu na poziomie żądania (metryka p50/p95) — gdy pytanie brzmi „czy użytkownik to odczuwa", a nie „która funkcja". Generator zamiast listy — gdy problemem jest szczyt zużycia pamięci, a nie czas: iteracja nie materializuje całego zbioru. `__slots__` w klasie — gdy obiektów jest milion i każdy niesie własny słownik atrybutów.

## Typowe błędy

- Optymalizowanie funkcji o najwyższym czasie skumulowanym zamiast własnym — na szczycie tej kolumny stoi zawsze wywołanie główne.
- Pojedynczy pomiar zamiast serii, przez co porównuje się wpływ stanu pamięci podręcznej, a nie wariantów kodu.
- Zgłoszenie poprawy bez liczby sprzed zmiany, czyli bez punktu odniesienia — poprawa staje się wtedy deklaracją.
- Profilowanie na danych o innej charakterystyce niż produkcyjne i przenoszenie wniosku wprost.
- Zostawienie `tracemalloc` włączonego na stałe i mierzenie odtąd narzutu własnego narzędzia.

## Pytania kontrolne

- pytanie: Profil pokazuje, że `main` ma 14,0 s czasu skumulowanego, `czysc_tekst` 12,4 s czasu własnego przy 1,2 mln wywołań, a `zapisz` 0,8 s. Co zmieniasz i jaką liczbę pokażesz jako dowód?
- odpowiedź: Zmieniam `czysc_tekst`, bo to jej czas własny stanowi prawie całość — `main` jest wysoko wyłącznie dlatego, że zawiera wszystko pozostałe. Liczba wywołań wskazuje na koszt na wywołanie, więc pierwszym krokiem jest wyniesienie pracy powtarzanej za każdym razem (kompilacja wyrażenia, budowa obiektu) poza pętlę. Dowodem jest ten sam profil na tym samym wejściu po zmianie: czas własny tej funkcji i czas całości przed i po.
- pytanie: Skąd wiesz, że optymalizacja zapisu do bazy nie ma tu sensu, mimo że intuicyjnie „baza jest wolna"?
- odpowiedź: Z udziału w profilu: 0,8 s z 13,4 s to 6% czasu, więc nawet sprowadzenie zapisu do zera skróci całość o mniej niż dziesiątą część. Górna granica zysku jest znana przed wykonaniem pracy i to ona, a nie intuicja, ustawia kolejność poprawek — dopiero po ścięciu dominującej pozycji baza może stać się nowym wąskim gardłem i wtedy warto ją zmierzyć ponownie.
- pytanie: Dlaczego czas z `cProfile` nie powinien być podawany jako bezwzględny wynik wydajności?
- odpowiedź: Profiler dodaje narzut przy każdym wywołaniu, szczególnie duży dla wielu krótkich funkcji, więc służy do znalezienia miejsca do zbadania; warianty porównuje się osobno tym samym pomiarem na tym samym wejściu.

## Źródła

- [The Python Profilers](https://docs.python.org/3/library/profile.html) — Python Software Foundation
- [timeit — Measure execution time of small code snippets](https://docs.python.org/3/library/timeit.html) — Python Software Foundation
- [tracemalloc — Trace memory allocations](https://docs.python.org/3/library/tracemalloc.html) — Python Software Foundation
