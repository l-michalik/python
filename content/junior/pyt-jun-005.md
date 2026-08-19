---
id: pyt-jun-005
title: Dostęp do bazy przez ORM
dependsOn: pyt-nic-006, pyt-nic-003
updated: 2026-08-14
---

## Polecenie

Zapisz i odczytaj rekord przez ORM i wskaż moment, w którym zmiana trafia do bazy.

## Odpowiedź

Klasę modelu odwzorowuje się na tabelę, a pracę wykonuje sesja: dodane i zmienione obiekty leżą w niej jako brudne, dopóki nie nastąpi opróżnienie (flush) wysyłające polecenia SQL i zatwierdzenie (commit) kończące transakcję. Odczyt buduje się jako obiekt zapytania i wykonuje na sesji. Zmiana schematu tabeli nie dzieje się przez edycję modelu — potrzebna jest migracja, czyli osobny, wersjonowany skrypt.

## Definicja

ORM (mapowanie obiektowo-relacyjne) tłumaczy klasy i ich atrybuty na tabele i kolumny, a operacje na obiektach na SQL. Sesja to jednostka pracy: śledzi obiekty, kolejkuje zmiany i wyznacza granicę transakcji. Migracja to plik opisujący przejście schematu bazy z jednej wersji do następnej, uruchamiany w tej samej kolejności na każdym środowisku.

## Zastosowanie

Bierze się to wszędzie tam, gdzie dane mają przeżyć restart procesu, a struktura jest z góry znana. To najczęstsze wymaganie techniczne w próbce po samym Pythonie: dziewięć ogłoszeń na trzynaście. ITDS pisze o „relational databases, especially PostgreSQL", emagine o „schema design and migrations", Fabrity o „znajomości relacyjnych baz danych oraz pracy z ORM", a DCG wprost o „PostgreSQL and SQLAlchemy".

## Jak to działa

Sesja trzyma mapę tożsamości: dla danego klucza głównego w jednej sesji istnieje dokładnie jeden obiekt Pythona, więc dwa odczyty tego samego wiersza zwracają ten sam obiekt. Zmiany atrybutów są zapisywane jako różnica i wysyłane dopiero przy opróżnieniu, które ORM wywołuje sam przed każdym zapytaniem — po to, żeby zapytanie zobaczyło twoje niezatwierdzone zmiany. Zatwierdzenie kończy transakcję i domyślnie unieważnia obiekty, więc kolejny dostęp do atrybutu wywoła nowy odczyt. Relacje są domyślnie ładowane leniwie: dostęp do `zamowienie.pozycje` wysyła osobne zapytanie w momencie sięgnięcia po atrybut, a nie przy odczycie zamówienia.

## Przykład

```python
with Session(engine) as sesja:
    z = Zamowienie(produkt="kabel", sztuk=3)
    sesja.add(z)
    sesja.commit()                      # dopiero tu INSERT trafia do bazy

    znalezione = sesja.scalars(
        select(Zamowienie).where(Zamowienie.sztuk > 1)
    ).all()
```

Gdyby po `add` a przed `commit` proces padł, w bazie nie zostanie nic — polecenie żyło w otwartej transakcji. Odwrotnie, `commit` bez `with` zostawia otwartą sesję i połączenie zajęte, co przy puli dwudziestu połączeń kończy się zablokowaną usługą.

## Ograniczenia

ORM ukrywa SQL, ale go nie usuwa: wygenerowane zapytanie bywa gorsze od napisanego ręcznie, a leniwe ładowanie relacji w pętli produkuje jedno zapytanie na iterację — problem, którego na tym poziomie nie widać, bo na dziesięciu rekordach testowych działa. Nie zdejmuje też potrzeby rozumienia indeksów i planu wykonania. Migracje generowane automatycznie z różnicy modeli bywają niepełne: zmiany typu kolumny i przeniesienia danych trzeba dopisać ręcznie.

## Alternatywy

Surowy SQL przez sterownik (`psycopg`) — gdy zapytanie jest złożone analitycznie i ORM tylko przeszkadza; kosztem jest ręczne mapowanie wyników. Warstwa pośrednia (SQLAlchemy Core) — te same zapytania budowane programowo, bez mapowania na klasy. ORM frameworka (Django ORM) — gdy i tak używa się Django, bo migracje i panel administracyjny są z nim zintegrowane. Kryterium: ORM do operacji na pojedynczych encjach, SQL do raportów i agregacji.

## Typowe błędy

- Trzymanie jednej sesji na całe życie aplikacji zamiast jednej na żądanie — obiekty starzeją się, a transakcja zostaje otwarta na godziny.
- `commit` w pętli po każdym rekordzie przy ładowaniu tysięcy wierszy, zamiast jednej transakcji na paczkę.
- Zmiana modelu bez migracji, przez co schemat na produkcji rozjeżdża się z kodem i awaria wychodzi dopiero przy wdrożeniu.
- Poleganie na leniwym ładowaniu w widoku listy, czyli wygenerowanie setek zapytań tam, gdzie wystarczyłoby jedno.
- Wstawianie wartości do zapytania przez sklejanie łańcuchów zamiast parametrów — otwarta droga do wstrzyknięcia SQL.

## Pytania kontrolne

- pytanie: Kod dodaje rekord i od razu czyta go zapytaniem w tej samej sesji, bez `commit`. Czy zapytanie go zobaczy i co to mówi o granicy transakcji?
- odpowiedź: Zobaczy — sesja opróżnia oczekujące zmiany przed wykonaniem zapytania, więc INSERT trafia do bazy wewnątrz otwartej transakcji. Nie znaczy to jednak, że rekord jest zapisany: inne połączenie go nie zobaczy, a wycofanie transakcji albo padnięcie procesu usuwa go bez śladu. Trwałość zaczyna się dopiero przy zatwierdzeniu.
- pytanie: Widok listy zamówień z ich pozycjami działa w teście na dziesięciu rekordach i muli na produkcji. Skąd wiesz, czy przyczyną jest ORM, i czym to sprawdzisz?
- odpowiedź: Włączam logowanie wysyłanych zapytań i liczę je dla jednego wywołania widoku. Liczba rosnąca proporcjonalnie do liczby zamówień oznacza leniwe ładowanie relacji wykonywane raz na iterację, a nie wolną bazę — ten sam kod na dziesięciu rekordach wysyła jedenaście zapytań i jest niezauważalny, na tysiącu wysyła tysiąc jeden.
- pytanie: Dlaczego zmiana modelu ORM nie wystarcza do zmiany tabeli na produkcji?
- odpowiedź: Model opisuje kod aplikacji, a istniejący schemat bazy zmienia wersjonowana migracja uruchamiana na każdym środowisku; bez niej aplikacja i tabela mają różne kontrakty.

## Źródła

- [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html) — SQLAlchemy
- [SQLAlchemy — PyPI](https://pypi.org/project/SQLAlchemy/) — Python Package Index
- [PostgreSQL: EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) — PostgreSQL Global Development Group
