---
id: pyt-jun-002
title: Adnotacje typów i mypy
dependsOn: pyt-nic-001, pyt-nic-004
updated: 2026-08-14
---

## Polecenie

Dodaj adnotacje typów do istniejącej funkcji i powiedz, co dzięki nim wyjdzie przed uruchomieniem, a co nie.

## Odpowiedź

Adnotacja to deklaracja, jakiego typu wartości funkcja przyjmuje i zwraca. Interpreter jej nie egzekwuje — jest metadanymi. Egzekwuje ją zewnętrzny sprawdzacz (mypy), uruchamiany jak linter, przed wykonaniem kodu. Wyjdzie z tego niezgodność deklaracji z użyciem: przekazany zły typ, brak obsługi `None`, literówka w nazwie atrybutu. Nie wyjdzie nic o danych, które program dostanie z zewnątrz w czasie działania.

## Definicja

Adnotacja typu (PEP 484) to zapis `def f(x: int) -> str`, przechowywany w atrybucie `__annotations__` funkcji. `Optional[T]`, zapisywane też jako `T | None`, oznacza wartość, która może być typu `T` albo pusta. Typ generyczny (`list[int]`, `dict[str, float]`) parametryzuje kontener typem elementu. mypy to statyczny sprawdzacz typów, który wnioskuje typy tam, gdzie ich nie zadeklarowano, i porównuje je z użyciem.

## Zastosowanie

Bierze się je do kodu, który przeżyje więcej niż jeden sprint, i przede wszystkim na granicach: sygnatury funkcji publicznych, modele danych, wartości zwracane z warstwy dostępu do bazy. emagine Polska stawia to wprost jako obowiązek — „Write strongly typed Python code (mypy)" — a Fabrity wymienia „Typowanie (Typing, Type Hints)" w jednym rzędzie z obsługą wyjątków. To jest odpowiedź języka na jego własną wadę z zagadnienia o dynamicznym typowaniu: przesuwa część błędów z czasu działania z powrotem przed uruchomienie.

## Jak to działa

mypy czyta kod bez jego uruchamiania, buduje graf typów i propaguje je przez przypisania i wywołania. Tam, gdzie typ zadeklarowano, przyjmuje deklarację; tam, gdzie nie, próbuje wywnioskować z kontekstu. Kod bez adnotacji jest domyślnie pomijany — funkcja bez sygnatury jest dla sprawdzacza nieprzezroczysta i nie zgłosi w niej żadnego błędu. Dlatego samo dodanie mypy do projektu bez adnotacji nie wykrywa niczego, a wynik rośnie stopniowo razem z pokryciem sygnaturami. Typ `Any` jest furtką wyłączającą sprawdzanie — każda wartość jest z nim zgodna, więc jego przypadkowe wpuszczenie cicho wyłącza kontrolę w całej gałęzi.

## Przykład

```python
def znajdz(uzytkownicy: dict[str, int], login: str) -> int | None:
    return uzytkownicy.get(login)

wiek = znajdz(dane, "ala") + 1     # mypy: unsupported operand type "None"
```

Bez adnotacji ta linia przejdzie sprawdzenie i wybuchnie w czasie działania dokładnie wtedy, gdy w słowniku zabraknie loginu — czyli na danych produkcyjnych, nie na testowych. Z adnotacją `int | None` sprawdzacz wymusza rozstrzygnięcie przypadku pustego przed dodawaniem.

## Ograniczenia

Adnotacje nie działają w czasie wykonania: przekazanie `str` tam, gdzie zadeklarowano `int`, nie rzuci wyjątku, bo interpreter deklaracji nie sprawdza. Nie chronią więc granicy z danymi zewnętrznymi — JSON z żądania HTTP wciąż wymaga walidacji w czasie działania. Biblioteka bez informacji o typach jest dla sprawdzacza `Any`, więc pokrycie kończy się na jej granicy. Sprawdzenie kosztuje czas w potoku CI i przy dużym projekcie liczy się w minutach.

## Alternatywy

Do walidacji danych wchodzących z zewnątrz — Pydantic, który z tych samych adnotacji generuje sprawdzenie wykonywane w czasie działania; to jest uzupełnienie mypy, nie zamiennik. Do sprawdzania typów w edytorze na bieżąco — Pyright, szybszy i domyślnie surowszy. Zamiast dziedziczenia po klasie bazowej dla zgodności typów — `Protocol`, czyli typ strukturalny. Kryterium: mypy pilnuje wnętrza programu, Pydantic jego granic.

## Typowe błędy

- Uruchomienie mypy na projekcie bez adnotacji, zobaczenie zera błędów i wniosek, że kod jest sprawdzony — funkcje bez sygnatur są domyślnie pomijane.
- Uciszanie ostrzeżeń przez `# type: ignore` bez kodu błędu, przez co komentarz zostaje na zawsze i ukrywa też błędy, które pojawią się później.
- Deklarowanie `Any`, żeby sprawdzacz przestał protestować — to wyłączenie kontroli, nie jej spełnienie.
- Traktowanie adnotacji jako walidacji danych z żądania i pominięcie sprawdzenia w czasie działania.

## Pytania kontrolne

- pytanie: Włączyłeś mypy w CI i dostałeś zero błędów na projekcie, w którym co tydzień wybucha `AttributeError` na `None`. Skąd wiesz, czy sprawdzenie w ogóle coś sprawdza?
- odpowiedź: Z raportu pokrycia adnotacjami, nie z liczby błędów — mypy domyślnie pomija funkcje bez sygnatur, więc zero może znaczyć „czysto" albo „nie ma czego czytać". Sprawdzam to, włączając tryb wymagający adnotacji dla definicji i patrząc, ile modułów nagle zaczyna zgłaszać braki; dopiero wtedy liczba błędów jest pomiarem, a nie artefaktem konfiguracji.
- pytanie: Funkcja ma sygnaturę `-> int`, a mimo to zwraca `None` i program działa. Dlaczego interpreter na to pozwolił?
- odpowiedź: Bo adnotacja jest metadanymi, a nie kontraktem egzekwowanym w czasie działania — interpreter zapisuje ją w `__annotations__` i nie sprawdza zgodności zwracanej wartości. Wyłapie to wyłącznie statyczny sprawdzacz uruchomiony osobno, i tylko wtedy, gdy w ogóle wejdzie w tę funkcję, czyli gdy ma ona sygnaturę.
- pytanie: Dlaczego `Any` jest ryzykowny w module objętym mypy?
- odpowiedź: `Any` jest zgodny ze wszystkim i propaguje się przez przypisania, więc może wyłączyć sprawdzanie całej gałęzi bez błędu; trzeba mierzyć jego wystąpienia na granicach z bibliotekami i danymi zewnętrznymi.

## Źródła

- [typing — Support for type hints](https://docs.python.org/3/library/typing.html) — Python Software Foundation
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/) — Python Software Foundation
- [Protocols and structural subtyping](https://mypy.readthedocs.io/en/stable/protocols.html) — mypy
