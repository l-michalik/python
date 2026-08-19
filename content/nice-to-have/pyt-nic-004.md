---
id: pyt-nic-004
title: Model obiektowy i wyjątki z lotu ptaka
updated: 2026-08-14
---

## Polecenie

Wyjaśnij, co znaczy zdanie „w Pythonie wszystko jest obiektem", i jak język sygnalizuje, że coś poszło nie tak.

## Odpowiedź

Każda wartość — liczba, funkcja, klasa, moduł — jest obiektem z typem i zestawem atrybutów, do których sięga się po nazwie. Sytuację wyjątkową język zgłasza, przerywając normalny przepływ i rzucając obiekt wyjątku, który leci w górę stosu wywołań aż do pierwszego bloku `except` gotowego go przyjąć; brak takiego bloku kończy program wypisaniem tracebacku, czyli ścieżki wywołań od miejsca uruchomienia do miejsca awarii.

## Definicja

Klasa to szablon opisujący, jakie atrybuty i metody ma obiekt danego typu. Dziedziczenie pozwala klasie przejąć zachowanie innej i je nadpisać. Wyjątek to obiekt reprezentujący sytuację, w której funkcja nie może zwrócić poprawnego wyniku; jest instancją klasy dziedziczącej z `BaseException` i sam podlega hierarchii dziedziczenia — dlatego `except OSError` przechwyci też `FileNotFoundError`.

## Zastosowanie

Klasy bierze się do modelowania pojęć domeny i do podmienialnych warstw dostępu — jeden interfejs, dwie implementacje. Wyjątki bierze się do sygnalizowania sytuacji, w których dalsze liczenie nie ma sensu, zamiast zwracania kodów błędu, które wywołujący może zignorować. Ogłoszenia ITDS („solid object-oriented programming fundamentals") i Fabrity („Programowanie obiektowe (OOP) i znajomość podstawowych wzorców projektowych", „Obsługa wyjątków") wymieniają jedno i drugie w tym samym punkcie.

## Jak to działa

Dostęp do atrybutu `obiekt.nazwa` jest wyszukiwaniem: interpreter zagląda najpierw do słownika samego obiektu, potem do jego klasy, potem do klas nadrzędnych w ustalonej kolejności. Dlatego metoda dopisana w podklasie przesłania odziedziczoną, a nie usuwa jej. Rzucenie wyjątku odwija stos: każda ramka wywołania jest zdejmowana i sprawdzana, czy stoi w niej pasujący `except`; ramki zdjęte po drodze trafiają do tracebacku, dzięki czemu widać nie tylko miejsce awarii, ale i drogę, którą się do niego doszło. Idiom Pythona nazywa się EAFP — łatwiej prosić o wybaczenie niż o pozwolenie: próbujesz wykonać operację i przechwytujesz wyjątek, zamiast sprawdzać wcześniej wszystkie warunki.

## Przykład

```python
class BrakDokumentu(Exception):
    pass

def wczytaj(sciezka):
    try:
        with open(sciezka) as f:
            return f.read()
    except FileNotFoundError as e:
        raise BrakDokumentu(sciezka) from e
```

Konstrukcja `raise ... from e` zamienia błąd techniczny na pojęcie z domeny i zachowuje pierwotną przyczynę — w tracebacku widać oba poziomy. Bez `from e` wywołujący dostaje informację, że dokumentu nie ma, ale traci informację, że przyczyną była nieistniejąca ścieżka, a nie brak uprawnień.

## Ograniczenia

Model obiektowy Pythona nie zapewnia hermetyzacji: podkreślnik przed nazwą atrybutu jest konwencją, a nie zakazem dostępu. Nie ma też deklarowanych interfejsów wymuszanych przez kompilator — zgodność sprawdza się dopiero przy wywołaniu. Wyjątki nie są częścią sygnatury funkcji, więc z samego jej nagłówka nie wynika, co może rzucić; tę wiedzę trzeba wyczytać z dokumentacji albo z kodu.

## Alternatywy

Zamiast klasy z samymi danymi — `dataclass` albo `NamedTuple`, które generują konstruktor i porównywanie. Zamiast dziedziczenia po wspólnej klasie bazowej — kompozycja i typ strukturalny (`Protocol`), gdy wspólne jest zachowanie, a nie pochodzenie. Zamiast wyjątku — zwrócenie wartości sygnalizującej brak (`None`, typ wynikowy), gdy sytuacja jest spodziewana i występuje często; wyjątki są kosztowne dopiero wtedy, gdy rzuca się je w pętli jako normalny przepływ sterowania.

## Typowe błędy

- `except Exception` bez ponownego rzucenia i bez logowania — błąd znika razem z informacją, gdzie powstał.
- Przechwytywanie wyjątku za szeroko i zbyt wcześnie, przez co warstwa niżej połyka problem, o którym warstwa wyżej musiałaby wiedzieć.
- Rzucanie gołego `Exception` zamiast klasy z domeny, przez co wywołujący nie ma czego przechwycić selektywnie.
- Gubienie pierwotnej przyczyny przez `raise NowyBlad(...)` bez `from`.

## Pytania kontrolne

- pytanie: Funkcja czytająca konfigurację przechwytuje `except Exception: return {}`. Co się w tym psuje i co zrobisz zamiast tego?
- odpowiedź: Pusty słownik jest nieodróżnialny od poprawnie wczytanej pustej konfiguracji, a przyczyna — literówka w ścieżce, brak uprawnień, błąd składni pliku — znika razem z tracebackiem. Zamiast tego przechwytuję konkretny wyjątek, którego się spodziewam, zamieniam go na błąd z domeny przez `raise ... from e` i pozwalam mu wyjść do warstwy, która umie zdecydować, czy program ma działać dalej.
- pytanie: Co znaczy w Pythonie zdanie „wszystko jest obiektem" i jaki ma to praktyczny skutek?
- odpowiedź: Znaczy, że funkcje, klasy i moduły są wartościami z typem i atrybutami, tak samo jak liczby. Praktyczny skutek jest taki, że funkcję można przekazać jako argument, podmienić w teście i trzymać w słowniku — nie potrzeba do tego osobnego mechanizmu, bo to zwykłe przypisanie nazwy do obiektu.
- pytanie: Dlaczego szerokie `except Exception` utrudnia diagnozę konfiguracji?
- odpowiedź: Zwraca tę samą wartość dla każdej przyczyny, ukrywając typ wyjątku i traceback; konkretny wyjątek przekazany dalej przez `raise ... from e` zachowuje przyczynę dla warstwy, która podejmie decyzję.

## Źródła

- [9. Classes](https://docs.python.org/3/tutorial/classes.html) — Python Software Foundation
- [8. Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) — Python Software Foundation
- [3. Data model](https://docs.python.org/3/reference/datamodel.html) — Python Software Foundation
