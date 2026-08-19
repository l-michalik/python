---
id: pyt-nic-005
title: Gdzie Python jest właściwą odpowiedzią, a gdzie nie
updated: 2026-08-14
---

## Polecenie

Rozstrzygnij, kiedy zadanie należy pisać w Pythonie, a kiedy trzeba sięgnąć po co innego, i nazwij mechanizm, który o tym decyduje.

## Odpowiedź

Rozstrzyga to, na co program zużywa czas. Jeśli czeka na sieć, dysk albo bazę danych — narzut interpretera ginie w tym czekaniu i Python jest właściwym wyborem. Jeśli liczy w pętli na procesorze, Python jest wolny, a dołożenie wątków nie pomoże, bo blokada globalnego interpretera (GIL) w domyślnej konfiguracji CPythona pozwala wykonywać bajtkod tylko jednemu wątkowi naraz.

## Definicja

Zadanie związane z wejściem-wyjściem (I/O-bound) to takie, w którym dominującym składnikiem czasu jest oczekiwanie na odpowiedź z zewnątrz. Zadanie związane z procesorem (CPU-bound) to takie, w którym dominuje liczenie. GIL to blokada wewnątrz CPythona gwarantująca, że w danej chwili bajtkod Pythona wykonuje jeden wątek — mechanizm chroniący spójność wewnętrznych struktur interpretera.

## Zastosowanie

To jest pytanie zadawane na rozmowie w postaci „dlaczego wasz serwis jest w Pythonie" i w postaci projektowej „przepisujemy ten moduł czy nie". Ogłoszenia Ntiative („Work across multiple technologies including Python, Go, Rust, C++") i CloudFerro (C++ i Golang obok Pythona w tym samym stacku) pokazują, że w praktyce odpowiedź brzmi „jedno i drugie" — a granicę trzeba umieć postawić.

## Jak to działa

Gdy wątek Pythona wykonuje operację wejścia-wyjścia, zwalnia GIL na czas oczekiwania — inne wątki mogą wtedy pracować. Dlatego sto równoległych żądań HTTP obsłużonych wątkami albo pętlą asynchroniczną skaluje się w Pythonie dobrze. Gdy wątek liczy, GIL trzyma i nie oddaje go poza krótkimi przełączeniami, więc cztery wątki liczące dzielą jeden rdzeń zamiast obsadzić cztery. Wyjścia są dwa: procesy zamiast wątków (każdy z własnym interpreterem i własnym GIL-em, kosztem serializacji danych między nimi) albo zejście do kodu, który zwalnia GIL na czas liczenia — tak działają NumPy i inne biblioteki z warstwą w C. Od Pythona 3.13 istnieje wariant interpretera bez GIL-a, a PEP 779 nadał mu w 3.14 status oficjalnie wspieranego — nie jest to jednak konfiguracja domyślna.

## Przykład

Serwis pobierający dane z dwudziestu API, każde odpowiada po 200 ms: wersja sekwencyjna zajmie około 4 s, wersja współbieżna — około 200 ms, bo cały ten czas to czekanie. Ten sam serwis liczący sumę kontrolną z 2 GB danych nie przyspieszy od dołożenia wątków ani o procent; przyspieszy dopiero od rozdzielenia pracy na procesy albo od oddania pętli bibliotece z warstwą natywną.

## Ograniczenia

Podział na I/O-bound i CPU-bound jest przybliżeniem: realne usługi robią jedno i drugie, a proporcja zmienia się z ruchem i z rozmiarem danych. Sam podział nie mówi też, ile dokładnie się zyska — do tego potrzebny jest pomiar, którego na tym poziomie się nie robi. Procesy zamiast wątków rozwiązują problem GIL-a, ale wprowadzają koszt uruchomienia i koszt przesłania danych, który przy małych zadaniach bywa większy niż zysk.

## Alternatywy

Do gorących pętli liczących wewnątrz projektu w Pythonie — rozszerzenie w C, Rust (PyO3) albo Cython, bez przepisywania całej usługi. Do zadań, gdzie liczenie jest całą treścią systemu — osobna usługa w Go lub C++. Do danych tabelarycznych — wypchnięcie pętli do silnika wektorowego (NumPy, Polars) albo rozproszonego (Spark, wymagany przez EPAM i TSS). Kryterium wyboru: czy pętla da się wyrazić jako operacja na całej tablicy — jeśli tak, przepisywanie języka jest przedwczesne.

## Typowe błędy

- Diagnoza „Python jest wolny" postawiona usłudze, która 95% czasu czeka na bazę danych.
- Dokładanie wątków do kodu liczącego i zdziwienie, że czas nie spadł.
- Przepisywanie całego serwisu na inny język, gdy kosztowna jest jedna funkcja.
- Traktowanie interpretera bez GIL-a jak gotowej odpowiedzi na wszystko — to wariant kompilacji, nie przełącznik, i nie każda biblioteka natywna jest w nim bezpieczna.

## Pytania kontrolne

- pytanie: Usługa w Pythonie obsługuje 300 równoczesnych żądań, z których każde czeka 150 ms na odpowiedź bazy, i zaczyna się dławić. Czy to jest argument za przepisaniem jej na Go?
- odpowiedź: Nie sam z siebie — to obciążenie jest oczekiwaniem, a nie liczeniem, więc GIL nie jest tu wąskim gardłem i przepisanie języka nie zaadresuje przyczyny. Najpierw sprawdzam, czy żądania są obsługiwane współbieżnie i czy nie kończy się pula połączeń do bazy; przepisanie ma sens dopiero wtedy, gdy dominującym składnikiem czasu okaże się praca procesora.
- pytanie: Dlaczego cztery wątki liczące w Pythonie nie dają czterokrotnego przyspieszenia, a cztery wątki pobierające dane z sieci dają?
- odpowiedź: Bo bajtkod Pythona wykonuje w danej chwili jeden wątek — pilnuje tego GIL. Wątek czekający na sieć zwalnia tę blokadę na czas oczekiwania, więc pozostałe mogą wtedy pracować i czasy oczekiwania się nakładają. Wątek liczący blokady nie oddaje, więc cztery takie wątki dzielą między siebie jeden rdzeń zamiast obsadzić cztery.
- pytanie: Jaki pomiar rozstrzyga, czy problem usługi jest obliczeniowy, czy wejścia-wyjścia?
- odpowiedź: Porównuję czas ścienny z czasem procesora przy rosnącej współbieżności: malejący czas ścienny przy prawie stałym procesora wskazuje oczekiwanie, a wartości zbliżone wskazują pracę obliczeniową.

## Źródła

- [Glossary — global interpreter lock](https://docs.python.org/3/glossary.html) — Python Software Foundation
- [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html) — Python Software Foundation
- [PEP 779 — Criteria for supported status for free-threaded Python](https://peps.python.org/pep-0779/) — Python Software Foundation
