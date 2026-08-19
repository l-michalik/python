---
id: pyt-reg-004
title: Wydajność warstwy ORM — N+1 i plan zapytania
dependsOn: pyt-jun-005, pyt-jun-001
updated: 2026-08-14
---

## Polecenie

Udowodnij liczbą, że wolny endpoint listy jest winą warstwy dostępu do danych, i wskaż, czy problemem jest liczba zapytań, czy jedno z nich.

## Odpowiedź

Liczysz zapytania wysłane w obsłudze jednego żądania. Liczba rosnąca proporcjonalnie do liczby wierszy to problem N+1 — leniwe ładowanie relacji wykonywane raz na element; leczy się go strategią ładowania z wyprzedzeniem. Liczba stała przy rosnącym czasie oznacza jedno wolne zapytanie i wtedy pytanie przenosi się do bazy: `EXPLAIN ANALYZE` pokazuje plan i to, czy wykonanie idzie po indeksie, czy przez skan całej tabeli.

## Definicja

Problem N+1 to wzorzec, w którym jedno zapytanie zwraca N wierszy, a dostęp do relacji każdego z nich wysyła kolejne zapytanie — łącznie N+1. Ładowanie z wyprzedzeniem (`selectinload`, `joinedload`) pobiera relację jednym dodatkowym zapytaniem albo złączeniem. Plan wykonania to opis, w jaki sposób baza zamierza policzyć wynik; `EXPLAIN ANALYZE` uruchamia zapytanie i podaje plan razem z faktycznymi czasami i liczbami wierszy.

## Zastosowanie

Bierze się to przy każdym widoku listy i przy każdym raporcie, bo tam różnica między dziesięcioma rekordami w teście a dziesięcioma tysiącami na produkcji jest różnicą jakościową. Dziewięć ogłoszeń w próbce wymaga pracy z bazą relacyjną, a cztery mówią wprost o wydajności: Fabrity o „optymalizacji zapytań do baz danych", Shelf o „performance tuning for real-time and high throughput scenarios", TSS o „optymalizacji zapytań i algorytmów", EPAM o „NFRs around high throughput and low latency".

## Jak to działa

Domyślna strategia relacji jest leniwa: obiekt nadrzędny wczytuje się bez potomnych, a zapytanie o nie idzie dopiero przy sięgnięciu po atrybut. W pętli po liście oznacza to jedno zapytanie na iterację, każde tanie z osobna i katastrofalne w sumie — koszt nie leży w bazie, tylko w liczbie obiegów sieciowych. `selectinload` zbiera klucze wszystkich rodziców i pobiera potomnych jednym zapytaniem z `IN`, dając stałe dwa zapytania niezależnie od N. `joinedload` robi to złączeniem w jednym zapytaniu, ale zwielokrotnia wiersze rodzica i przy relacji jeden-do-wielu potrafi przesłać wielokrotnie więcej danych. Po stronie bazy `EXPLAIN ANALYZE` pokazuje, czy planer wybrał skan indeksu, czy sekwencyjny, i porównuje szacowaną liczbę wierszy z faktyczną — duża rozbieżność zwykle znaczy nieaktualne statystyki albo brak indeksu na kolumnie filtru.

## Przykład

Widok listy stu zamówień z pozycjami, logowanie SQL włączone:

```
domyślnie (leniwie):   101 zapytań, 100 rekordów,  łącznie 1,9 s
selectinload:            2 zapytania, 100 rekordów, łącznie 0,05 s
```

Przy tysiącu zamówień pierwsza wersja wysyła 1001 zapytań i przekracza czas odpowiedzi, druga wciąż wysyła dwa. Jeśli po tej zmianie jedno z dwóch zapytań nadal trwa sekundę, dowodem drugiego rodzaju jest plan: `Seq Scan on pozycje (actual rows=2400000)` przy filtrze na kolumnie bez indeksu.

## Ograniczenia

Ładowanie z wyprzedzeniem przesuwa koszt, nie usuwa go: pobranie relacji, których widok nie użyje, marnuje pamięć i czas transferu. `joinedload` przy dwóch relacjach jeden-do-wielu naraz mnoży wiersze kartezjańsko. Liczba zapytań nie jest miarą wystarczającą — jedno źle napisane zapytanie bywa gorsze niż sto prostych. `EXPLAIN` bez `ANALYZE` pokazuje wyłącznie plan i szacunki, nie faktyczne czasy, a plan zależy od statystyk i rozmiaru tabeli, więc wynik z bazy deweloperskiej z tysiącem wierszy nie przenosi się na produkcję.

## Alternatywy

Zapytanie ręczne w SQL zwracające gotowy zestaw kolumn — gdy widok potrzebuje pięciu pól z trzech tabel, a ORM materializuje pełne encje. Paginacja po kluczu zamiast po przesunięciu (`OFFSET`) — gdy strona tysięczna jest równie wolna jak wszystkie poprzednie razem. Widok zmaterializowany albo tabela zagregowana — gdy raport liczy to samo przy każdym wejściu. Pamięć podręczna na poziomie odpowiedzi — gdy dane zmieniają się rzadziej, niż są czytane, i wolno je pokazać nieświeże.

## Typowe błędy

- Uznanie, że problemem jest wolna baza, bez policzenia zapytań — przy N+1 baza jest szybka, a wolne są obiegi.
- Zamiana wszystkich relacji na ładowanie zachłanne „na wszelki wypadek", co zamienia problem N+1 na przesyłanie danych, których nikt nie użyje.
- Testowanie wydajności na bazie z tysiącem wierszy, gdzie planer wybiera inny plan niż na milionie.
- Dodanie indeksu bez sprawdzenia planu — indeks na kolumnie o małej selektywności nie zostanie użyty, a spowolni zapis.
- Paginacja przez duży `OFFSET`, przy której baza i tak przechodzi wszystkie pominięte wiersze.

## Pytania kontrolne

- pytanie: Endpoint listy odpowiada w 1,9 s. W logu widzisz 101 zapytań na jedno żądanie przy stu rekordach. Co to rozstrzyga i jaką liczbę pokażesz po poprawce?
- odpowiedź: Rozstrzyga, że kosztem jest liczba obiegów, a nie pojedyncze zapytanie — sto jeden przy stu rekordach to podpis leniwego ładowania relacji w pętli. Po zmianie strategii na ładowanie z wyprzedzeniem pokazuję dwie liczby zmierzone tak samo: liczbę zapytań (2, stała względem N) i czas odpowiedzi. Jeśli czas nie spadł proporcjonalnie, pozostaje drugi rodzaj problemu i przenoszę pomiar do planu zapytania.
- pytanie: Po naprawie N+1 zostały dwa zapytania, ale jedno trwa 900 ms. Skąd wiesz, czy winny jest brak indeksu?
- odpowiedź: Z `EXPLAIN ANALYZE` tego zapytania na bazie o produkcyjnym rozmiarze: skan sekwencyjny po dużej tabeli przy wąskim filtrze wskazuje na brak indeksu, a duża rozbieżność między szacowaną a faktyczną liczbą wierszy — na nieaktualne statystyki. Sam czas o tym nie mówi, bo to samo 900 ms może pochodzić z przesłania nadmiarowych kolumn albo ze złączenia mnożącego wiersze.
- pytanie: Kiedy `joinedload` może pogorszyć wynik mimo zmniejszenia liczby zapytań?
- odpowiedź: Przy relacjach jeden-do-wielu złączenie powiela wiersze rodzica, a przy kilku takich relacjach mnożenie rośnie kartezjańsko; trzeba wtedy zmierzyć rozmiar wyniku i rozważyć `selectinload`.

## Źródła

- [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html) — SQLAlchemy
- [PostgreSQL: EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) — PostgreSQL Global Development Group
- [SQLAlchemy — PyPI](https://pypi.org/project/SQLAlchemy/) — Python Package Index
