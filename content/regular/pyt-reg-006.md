---
id: pyt-reg-006
title: Typowanie strict, protokoły i granice sprawdzenia
dependsOn: pyt-jun-002, pyt-jun-004
updated: 2026-08-14
---

## Polecenie

Podnieś surowość sprawdzania typów w istniejącym projekcie i pokaż, po czym poznasz, że przyniosło to efekt.

## Odpowiedź

Surowość włącza się stopniowo, moduł po module, a nie globalnym przełącznikiem — inaczej dostaje się kilka tysięcy zgłoszeń naraz i wyłącza się je z powrotem. Efekt mierzy się dwiema liczbami: odsetkiem kodu, który sprawdzacz w ogóle analizuje (funkcje bez sygnatur są domyślnie pomijane), oraz liczbą wyciszeń `type: ignore` i wystąpień `Any` na granicach. Sama liczba błędów bez tych dwóch jest artefaktem konfiguracji, nie pomiarem.

## Definicja

Tryb `strict` w mypy to zestaw flag włączanych razem: wymaganie adnotacji dla wszystkich definicji, zakaz niejawnego `Any`, zakaz wywołań funkcji nieotypowanych, ostrzeżenia o zbędnych rzutowaniach i nieosiągalnym kodzie. `Protocol` to typ strukturalny: zgodność sprawdza się po zestawie metod, a nie po dziedziczeniu. Typ generyczny parametryzowany zmienną typu pozwala zachować związek między typem wejścia a typem wyjścia.

## Zastosowanie

Bierze się to w kodzie, który ma wiele wywołujących i długi cykl życia — bibliotekach wewnętrznych, warstwie dostępu do danych, kontraktach między modułami. emagine Polska wymaga wprost „strongly typed Python code (mypy)", Fabrity wymienia typowanie obok czytelności kodu, ITDS mówi o „solid object-oriented programming fundamentals". Na tym poziomie różnica względem poziomu niżej polega na tym, że typy przestają być ozdobą sygnatury, a zaczynają wyrażać kontrakt, którego nie da się spełnić przypadkiem.

## Jak to działa

Sprawdzacz analizuje moduł po module i dla każdego decyduje, czy w ogóle w niego wchodzi: funkcja bez adnotacji jest domyślnie nieanalizowana, a wartość zwracana z nieotypowanej biblioteki jest `Any`, który jest zgodny ze wszystkim. `Any` propaguje się wzdłuż przypisań, więc jedna nieotypowana granica potrafi wyłączyć sprawdzanie w całym poddrzewie wywołań — i to jest mechanizm, przez który projekt z mypy w CI może nie sprawdzać niczego. Konfiguracja per moduł pozwala domknąć to stopniowo: surowość włącza się tam, gdzie kod jest już otypowany, a wyjątki zapisuje się jawnie w `pyproject.toml`, zamiast rozsypywać komentarze po plikach. `Protocol` rozwiązuje przy tym typowy konflikt: dwie klasy z tym samym zestawem metod pasują do wspólnego typu bez wprowadzania sztucznej klasy bazowej i bez zależności między modułami.

## Przykład

```python
from typing import Protocol

class Repozytorium(Protocol):
    def pobierz(self, klucz: str) -> bytes | None: ...

def obsluz(repo: Repozytorium, klucz: str) -> int:
    dane = repo.pobierz(klucz)
    return len(dane)          # mypy: Item "None" has no attribute "__len__"
```

Ani `RepozytoriumS3`, ani `RepozytoriumDysk` nie muszą po niczym dziedziczyć — wystarczy, że mają metodę o tej sygnaturze. Sprawdzenie łapie przy okazji brak obsługi wartości pustej. Typowy odczyt po włączeniu surowości na jednym module: 34 zgłoszenia, z czego 21 to brakujące adnotacje, 9 to nieobsłużony `None`, 4 to wywołania biblioteki bez informacji o typach — i tylko te ostatnie kwalifikują się do wyciszenia.

## Ograniczenia

Sprawdzenie statyczne nie chroni granicy z danymi zewnętrznymi: JSON z żądania, wiersz z bazy i odpowiedź modelu językowego wymagają walidacji w czasie działania niezależnie od tego, jak surowa jest konfiguracja. Biblioteki bez pakietu z informacjami o typach zostają `Any` i domykają się dopiero pakietami `types-*` albo własnymi zaślepkami. Tryb `strict` na starym kodzie generuje pracę, która nie zawsze jest opłacalna — moduł, który za kwartał zniknie, nie musi być otypowany. Czas sprawdzenia rośnie z projektem i przy dużym repozytorium liczy się w minutach na każdym scaleniu.

## Alternatywy

Pyright — szybszy i domyślnie surowszy, z lepszą obsługą typów w edytorze; różni się interpretacją części przypadków, więc mieszanie obu w jednym projekcie generuje sprzeczne zgłoszenia. Pydantic — do granic z danymi zewnętrznymi, bo z tych samych adnotacji buduje walidację działającą w czasie wykonania. Klasa bazowa abstrakcyjna zamiast `Protocol` — gdy zależy na jawnej deklaracji zgodności i wspólnej implementacji. Kryterium: mypy w potoku CI jako brama, Pydantic na wejściu, `Protocol` w miejscach, gdzie zależność w drugą stronę byłaby cyklem.

## Typowe błędy

- Włączenie `strict` globalnie na całym repozytorium, wygenerowanie tysięcy zgłoszeń i wyłączenie go tydzień później.
- Traktowanie liczby błędów mypy jako miary jakości bez sprawdzenia, jaki odsetek kodu jest w ogóle analizowany.
- Wyciszanie zgłoszeń przez `# type: ignore` bez kodu błędu, przez co komentarz ukrywa również błędy pojawiające się później.
- Wprowadzanie klasy bazowej wyłącznie po to, żeby dwa moduły miały wspólny typ — `Protocol` załatwia to bez zależności.
- Poleganie na adnotacjach jako walidacji danych wejściowych i pominięcie sprawdzenia w czasie działania.

## Pytania kontrolne

- pytanie: Projekt ma mypy w CI, zero błędów i regularne awarie typu „NoneType has no attribute". Jak sprawdzisz, czy sprawdzenie w ogóle działa, i jaką liczbę pokażesz zespołowi?
- odpowiedź: Włączam wymaganie adnotacji dla definicji na wybranym module i porównuję liczbę analizowanych funkcji przed i po — zero błędów przy niskim pokryciu sygnaturami znaczy, że sprawdzacz pomija większość kodu, a nie że kod jest poprawny. Liczbą do pokazania jest odsetek funkcji z adnotacjami oraz liczba wystąpień `Any` i wyciszeń na granicach, bo to one wyznaczają realny zasięg sprawdzenia.
- pytanie: Dwie klasy z różnych modułów mają tę samą metodę i chcesz je przyjmować w jednej funkcji. Dlaczego `Protocol` jest tu lepszy niż wspólna klasa bazowa?
- odpowiedź: Bo zgodność z protokołem sprawdza się po kształcie, więc żaden z modułów nie musi importować drugiego ani wspólnego przodka — nie powstaje zależność, którą trzeba by potem rozplątywać przy cyklu importów. Klasa bazowa ma przewagę tam, gdzie oprócz kontraktu ma być współdzielona implementacja; przy samym kontrakcie dokłada wyłącznie sprzężenie.
- pytanie: Dlaczego `strict` włącza się modułami, a nie jednym przełącznikiem dla starego projektu?
- odpowiedź: Globalne włączenie daje naraz tysiące zgłoszeń, które zwykle kończą się wyłączeniem reguły; konfiguracja per moduł pozwala domykać sprawdzanie tam, gdzie sygnatury są gotowe.

## Źródła

- [Protocols and structural subtyping](https://mypy.readthedocs.io/en/stable/protocols.html) — mypy
- [typing — Support for type hints](https://docs.python.org/3/library/typing.html) — Python Software Foundation
- [mypy — PyPI](https://pypi.org/project/mypy/) — Python Package Index
