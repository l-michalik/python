---
id: pyt-nic-003
title: Wbudowane struktury danych i ich koszt
updated: 2026-08-14
---

## Polecenie

Wskaż, czym różnią się lista, słownik, zbiór i krotka, i po czym poznajesz, że wybrałeś złą.

## Odpowiedź

Lista trzyma kolejność i pozwala na duplikaty, ale sprawdzenie „czy zawiera X" wymaga przejrzenia wszystkich elementów. Słownik i zbiór są zbudowane na tablicy mieszającej, więc to samo sprawdzenie jest niezależne od liczby elementów, w zamian za wymóg, żeby klucz był niemutowalny. Krotka to lista, której nie da się zmienić — i właśnie dlatego może być kluczem słownika. Zła struktura poznaje się po tym, że czas działania rośnie szybciej niż dane.

## Definicja

Lista (`list`) to uporządkowana, zmienna sekwencja o dostępie po indeksie. Słownik (`dict`) to odwzorowanie klucz → wartość oparte na skrócie (hashu) klucza, zachowujące kolejność wstawiania. Zbiór (`set`) to nieuporządkowana kolekcja unikalnych elementów, również oparta na skrócie. Krotka (`tuple`) to niemutowalna sekwencja — po utworzeniu nie da się jej zmienić, więc ma stabilny skrót.

## Zastosowanie

Wybór struktury jest pierwszą decyzją wydajnościową w programie i zapada zanim ktokolwiek pomyśli o profilerze. Ogłoszenia CloudFerro („dobre podstawy algorytmów i struktur danych"), Ntiative („solid understanding of software architecture, algorithms, and data structures") i TSS („optymalizacja zapytań i algorytmów przetwarzających duże zbiory danych") pytają dokładnie o to: czy kandydat wie, kiedy lista jest złą odpowiedzią.

## Jak to działa

Lista to ciągły blok wskaźników: dostęp po indeksie jest natychmiastowy, ale wyszukiwanie po wartości musi porównać element po elemencie, więc koszt rośnie liniowo z długością. Słownik i zbiór liczą skrót elementu i na jego podstawie wyznaczają miejsce w tablicy — koszt sprawdzenia nie zależy od liczby elementów, dopóki skróty rozkładają się równomiernie. Ceną jest wymóg niemutowalności klucza: gdyby klucz dało się zmienić po wstawieniu, jego skrót przestałby wskazywać na miejsce, w którym leży, i wartość zniknęłaby ze słownika mimo że wciąż w nim siedzi.

## Przykład

Filtrowanie miliona identyfikatorów po liście dozwolonych:

```python
dozwolone = [1, 7, 13, ...]        # 10 000 elementów
wynik = [x for x in dane if x in dozwolone]

dozwolone = {1, 7, 13, ...}        # ten sam zbiór jako set
wynik = [x for x in dane if x in dozwolone]
```

Pierwsza wersja wykonuje do 10 000 porównań na każdy element `dane` — przy milionie elementów to rząd 10 miliardów operacji. Druga liczy jeden skrót na element. Zmiana jednego znaku w kodzie, różnica rzędu wielkości w czasie.

## Ograniczenia

Tablica mieszająca kupuje szybkość pamięcią: zbiór zajmuje wyraźnie więcej niż lista tych samych elementów, bo musi trzymać rzadko zapełnioną tablicę. Nie zachowuje kolejności sortowania — kolejność wstawiania w słowniku to nie to samo co uporządkowanie. Elementy muszą być haszowalne, więc listy i słowniki nie mogą być kluczami. Przy dużych zbiorach liczb ani lista, ani zbiór nie są właściwą strukturą, bo każdy element jest osobnym obiektem z własnym nagłówkiem.

## Alternatywy

Gdy potrzebne jest wstawianie i zdejmowanie z obu końców — `collections.deque`, bo wstawianie na początek listy przesuwa całą resztę. Gdy elementy mają być stale posortowane — lista utrzymywana przez `bisect` albo kopiec z `heapq`. Gdy danych jest tyle, że liczy się rozmiar w pamięci — tablica jednorodna (`array`, NumPy) zamiast listy obiektów. Gdy struktura ma nazwane pola i ma być niemutowalna — `NamedTuple` albo `dataclass(frozen=True)`.

## Typowe błędy

- Sprawdzanie przynależności (`in`) na liście wewnątrz pętli po drugim dużym zbiorze — klasyczny sposób na przypadkowy koszt kwadratowy.
- Używanie listy jako kolejki i zdejmowanie z jej początku (`pop(0)`), co przesuwa wszystkie pozostałe elementy przy każdym zdjęciu.
- Zakładanie, że zbiór zachowa kolejność, bo w małym przykładzie wyszła zgodna z wstawianiem.
- Mutowalna wartość domyślna argumentu (`def f(x=[])`) — lista powstaje raz, przy definicji funkcji, i jest współdzielona przez wszystkie wywołania.

## Pytania kontrolne

- pytanie: Skrypt sprawdza dla każdego z miliona rekordów, czy jego identyfikator jest na liście dziesięciu tysięcy dozwolonych, i działa kilkanaście minut. Co zmieniasz i dlaczego to pomoże?
- odpowiedź: Zamieniam listę dozwolonych na zbiór. Sprawdzenie `in` na liście przegląda elementy po kolei, więc koszt to iloczyn obu liczności; na zbiorze sprowadza się do policzenia skrótu i jednego zajrzenia do tablicy, niezależnie od tego, ile elementów zbiór ma. Zmienia się rząd kosztu, a nie stała — dlatego efekt jest widoczny, a nie kosmetyczny.
- pytanie: Dlaczego krotka może być kluczem słownika, a lista nie?
- odpowiedź: Bo klucz musi mieć stabilny skrót przez cały czas, gdy leży w słowniku — miejsce w tablicy mieszającej wyznacza się właśnie z niego. Krotki nie da się zmienić po utworzeniu, więc jej skrót jest stały; lista jest mutowalna, więc jej skrót przestałby pasować do miejsca, w którym ją zapisano, i wpis stałby się nieosiągalny.
- pytanie: Kiedy zamiana listy na zbiór nie jest właściwą optymalizacją?
- odpowiedź: Gdy potrzebujesz zachować kolejność albo duplikaty, bo zbiór przechowuje tylko unikalne wartości i nie reprezentuje kolejności wejścia; wybiera się go dla szybkiego sprawdzania przynależności.

## Źródła

- [5. Data Structures](https://docs.python.org/3/tutorial/datastructures.html) — Python Software Foundation
- [TimeComplexity](https://wiki.python.org/moin/TimeComplexity) — Python Software Foundation
- [3. Data model](https://docs.python.org/3/reference/datamodel.html) — Python Software Foundation
