---
id: pyt-jun-003
title: Testy jednostkowe w pytest
dependsOn: pyt-nic-004, pyt-nic-002
updated: 2026-08-14
---

## Polecenie

Napisz zestaw testów dla funkcji z dwoma przypadkami brzegowymi i wyjaśnij, skąd biorą się dane wejściowe do każdego z nich.

## Odpowiedź

W pytest test to zwykła funkcja o nazwie zaczynającej się od `test_`, w której warunek sprawdza się gołym `assert`. Powtarzalne przygotowanie danych wyciąga się do fixture — funkcji oznaczonej `@pytest.fixture`, którą test przyjmuje jako argument. Wiele wariantów tych samych danych opisuje się `@pytest.mark.parametrize`, żeby nie kopiować ciała testu. Przypadki brzegowe biorą się z granic dziedziny funkcji: pusty wejściowy zbiór, wartość skrajna, dane niepoprawne.

## Definicja

Test jednostkowy sprawdza pojedynczy kawałek logiki w izolacji od bazy danych, sieci i zegara. Fixture to nazwany zasób budowany przed testem i sprzątany po nim, którego cykl życia (`function`, `module`, `session`) ustala się parametrem `scope`. Parametryzacja mnoży jeden test przez listę zestawów argumentów, dając osobny wynik dla każdego z nich.

## Zastosowanie

Bierze się to do kodu, który ktoś będzie zmieniał — test jest jedynym mechanizmem, który przy zmianie mówi, co się przy okazji zepsuło. CloudFerro wymaga „pisania testów jednostkowych zgodnie z TDD", DCG „automated tests, preferably with pytest", a Fabrity wymienia je razem z code review jako element dbałości o jakość kodu. W próbce rynkowej wymóg pojawia się w ośmiu ogłoszeniach na trzynaście.

## Jak to działa

pytest zbiera pliki pasujące do wzorca `test_*.py`, importuje je i wyszukuje funkcje `test_*`. Argumenty każdej takiej funkcji traktuje jako nazwy fixture i rozwiązuje je rekurencyjnie — fixture może żądać innych fixture. Przed asercją przepisuje kod bajtowy tak, żeby po niepowodzeniu pokazać wartości pośrednie: dlatego `assert wynik == 5` wypisuje, ile faktycznie wyszło, bez pisania własnego komunikatu. Zakres fixture decyduje, ile razy zasób powstaje: `function` buduje go dla każdego testu z osobna, `session` raz na całe uruchomienie — co jest szybsze, ale przecieka stan między testami.

## Przykład

```python
import pytest
from platforma.rabat import policz

@pytest.mark.parametrize(
    ("kwota", "procent", "oczekiwane"),
    [(100, 0, 100), (100, 100, 0), (0, 50, 0), (99.99, 10, 89.99)],
)
def test_policz(kwota, procent, oczekiwane):
    assert policz(kwota, procent) == pytest.approx(oczekiwane)

def test_odrzuca_ujemny_procent():
    with pytest.raises(ValueError):
        policz(100, -1)
```

Cztery zestawy to nie cztery losowe liczby: zero i sto procent to granice dziedziny, zero jako kwota to przypadek pusty, a `99.99` wchodzi tam, bo działanie na liczbach zmiennoprzecinkowych nie daje dokładnej równości — stąd `approx` zamiast `==`.

## Ograniczenia

Test jednostkowy nie powie nic o tym, czy komponenty złożone razem współpracują — na to potrzebny jest test integracyjny z prawdziwą bazą. Nie wykryje też błędu, którego przypadku nikt nie wymyślił: zestaw testów sprawdza wyobraźnię autora, nie przestrzeń wejść. Fixture o zakresie szerszym niż `function` wprowadza kolejność zależności między testami, więc awaria potrafi zależeć od tego, które testy uruchomiono wcześniej.

## Alternatywy

`unittest` z biblioteki standardowej — gdy nie wolno dokładać zależności; kosztem jest składnia klasowa i własne metody asercji. Testy własnościowe (Hypothesis) — gdy przypadki brzegowe trudno wymyślić, bo biblioteka generuje je sama i minimalizuje kontrprzykład. `doctest` — gdy przykład w dokumentacji ma być jednocześnie testem. Kryterium: pytest do reguły, Hypothesis do funkcji czystych o dużej przestrzeni wejść.

## Typowe błędy

- Test sprawdzający implementację zamiast zachowania — pada przy każdej refaktoryzacji, mimo że program działa tak samo.
- Fixture o zakresie `session` trzymająca stan mutowalny, przez co kolejność testów zaczyna mieć znaczenie.
- Test bez asercji, który przechodzi zawsze, bo mierzy wyłącznie brak wyjątku.
- Sprawdzanie równości liczb zmiennoprzecinkowych operatorem `==` zamiast tolerancji.
- Mockowanie wszystkiego, aż test potwierdza wyłącznie to, że mocki zostały wywołane.

## Pytania kontrolne

- pytanie: Test przechodzi uruchomiony pojedynczo, a pada przy uruchomieniu całego zestawu. Jaka jest najbardziej prawdopodobna przyczyna i jak ją potwierdzisz?
- odpowiedź: Stan przeciekający między testami — najczęściej fixture o zakresie `module` lub `session` trzymająca obiekt mutowalny, albo zmienna globalna modyfikowana przez wcześniejszy test. Potwierdzam, zawężając zakres tej fixture do `function` i sprawdzając, czy problem znika; jeśli tak, przyczyną była współdzielona instancja, a nie sama kolejność.
- pytanie: Skąd biorą się cztery zestawy w parametryzacji z przykładu i co byś zmienił, gdyby funkcja przyjmowała procent jako liczbę całkowitą z zakresu 0–100?
- odpowiedź: Z granic dziedziny: zero i sto procent to końce przedziału, zerowa kwota to przypadek pusty, a wartość niecałkowita wymusza porównanie z tolerancją zamiast równości. Przy procencie całkowitym zestaw z `99.99` traci sens jako test zaokrąglenia wejścia i zastąpiłbym go wartościami tuż za granicą — `-1` i `101` — sprawdzającymi, że funkcja je odrzuca, bo to tam przebiega nowy kontrakt.
- pytanie: Kiedy fixture o zakresie `session` jest niebezpieczna dla testów jednostkowych?
- odpowiedź: Gdy udostępnia stan mutowalny, bo jeden test może zmienić go dla kolejnego i wynik zacznie zależeć od kolejności; taki zasób trzeba tworzyć per test albo czyścić pomiędzy przypadkami.

## Źródła

- [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) — pytest
- [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html) — pytest
- [The Python Standard Library](https://docs.python.org/3/library/index.html) — Python Software Foundation
