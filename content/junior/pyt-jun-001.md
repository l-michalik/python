---
id: pyt-jun-001
title: Środowisko i zależności projektu
dependsOn: pyt-nic-002, pyt-nic-006
updated: 2026-08-14
---

## Polecenie

Załóż projekt tak, żeby ktoś inny odtworzył u siebie dokładnie te same wersje zależności, i wskaż, który plik to gwarantuje.

## Odpowiedź

Zależności deklaruje się w `pyproject.toml` — tam idą nazwy pakietów i dopuszczalne zakresy wersji. Odtwarzalność daje dopiero plik blokady (`uv.lock`, `requirements.txt` z przypiętymi wersjami), który zapisuje konkretne wersje wszystkich pakietów razem z zależnościami przechodnimi. Deklaracja mówi „czego potrzebuję", blokada mówi „co u mnie zadziałało" — do repozytorium wchodzą oba.

## Definicja

`pyproject.toml` to standardowy plik konfiguracji projektu: metadane, lista zależności głównych, grupy zależności deweloperskich i konfiguracja narzędzi. Plik blokady to wygenerowany zapis rozwiązanego drzewa zależności z dokładnymi wersjami i sumami kontrolnymi. `uv` to menedżer, który jednym poleceniem tworzy środowisko, rozwiązuje zależności i zapisuje blokadę; `ruff` to linter i formater konfigurowany w tym samym pliku.

## Zastosowanie

Bierze się to natychmiast po utworzeniu katalogu projektu, przed pierwszą linią kodu — bo dopisanie deklaracji po fakcie oznacza rekonstruowanie z pamięci, co się instalowało. ITDS wymaga wprost „modern Python tooling (uv, Ruff, Rye)", emagine Polska „automated checks (ruff, pytest)", a Fabrity „pracy z modułami i pakietami". To jest też warunek wstępny konteneryzacji: obraz Dockera buduje się z pliku blokady, nie z pamięci autora.

## Jak to działa

Menedżer zależności czyta deklarowane zakresy, pobiera metadane pakietów z PyPI i rozwiązuje układ równań: dobiera taki zestaw wersji, żeby wszystkie ograniczenia — również te wniesione przez zależności zależności — dały się spełnić naraz. Wynik zapisuje w blokadzie razem z sumami kontrolnymi plików. Instalacja z blokady pomija cały etap rozwiązywania: bierze wypisane wersje i sprawdza sumy. Dlatego dwa uruchomienia z tej samej blokady dają identyczne środowisko, a dwa uruchomienia z samej deklaracji — niekoniecznie, bo w międzyczasie mogło wyjść nowe wydanie mieszczące się w zakresie.

## Przykład

```toml
[project]
name = "platforma"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.141,<0.142",
    "sqlalchemy>=2.0,<3.0",
]

[dependency-groups]
dev = ["pytest>=9.1", "mypy>=2.3", "ruff>=0.16"]

[tool.ruff]
line-length = 100
```

Zapis `>=2.0,<3.0` dla SQLAlchemy przepuszcza wydania poprawkowe (2.0.52 zamiast 2.0.40), ale zatrzymuje się przed 3.0, gdzie zgodność wsteczna nie jest obiecana. Blokada zapisze, że dziś zainstalowało się dokładnie 2.0.52.

## Ograniczenia

Blokada zapewnia te same wersje pakietów, ale nie tę samą wersję interpretera (to osobna deklaracja `requires-python` i osobne narzędzie), nie te same biblioteki systemowe pod pakietami binarnymi i nie ten sam system operacyjny. Nie chroni też przed pakietem, który został z PyPI wycofany — suma kontrolna zgadza się tylko wtedy, gdy plik nadal tam jest. Przypięcie wszystkiego na sztywno w deklaracji, zamiast w blokadzie, blokuje z kolei poprawki bezpieczeństwa.

## Alternatywy

`pip` z `requirements.txt` — działa wszędzie i nie wymaga niczego poza standardem, ale rozwiązywanie zależności jest wolniejsze, a plik blokady trzeba wygenerować osobnym narzędziem. Poetry — pełny menedżer projektu z własnym formatem blokady, dojrzalszy ekosystemem wtyczek. Conda — gdy zależności wychodzą poza Pythona (biblioteki numeryczne, sterowniki). Kryterium: `uv` przy nowym projekcie i nacisku na czas budowania, `pip` gdy nie wolno dokładać narzędzi spoza standardu.

## Typowe błędy

- Trzymanie w repozytorium samej deklaracji bez blokady i zdziwienie, że „u mnie działa" — u kogoś innego zainstalowała się nowsza wersja zależności przechodniej.
- Przypinanie wszystkich wersji na sztywno w `pyproject.toml`, przez co żadna aktualizacja bezpieczeństwa nie wchodzi bez ręcznej edycji.
- Mieszanie zależności deweloperskich z produkcyjnymi — obraz produkcyjny wiezie wtedy pytest i mypy.
- Aktualizacja blokady „przy okazji" innej zmiany, przez co przegląd kodu nie odróżnia zmiany logiki od skoku o trzydzieści wersji.

## Pytania kontrolne

- pytanie: W `pyproject.toml` stoi `sqlalchemy>=2.0,<3.0`. Skąd bierze się dolna i górna granica tego zakresu i co się zepsuje, jeśli zapiszesz `sqlalchemy>=2.0` bez górnej?
- odpowiedź: Dolna granica to wersja, od której istnieje API, którego używasz; górna to pierwsza wersja główna, dla której nie obiecano zgodności wstecznej. Bez górnej granicy dzień wydania 3.0 staje się dniem, w którym świeża instalacja wciąga niezgodną bibliotekę i budowanie pada bez żadnej zmiany w twoim kodzie — a przy braku pliku blokady dotyczy to również produkcji.
- pytanie: Testy przechodzą u ciebie i padają w CI na braku atrybutu w bibliotece. Od czego zaczynasz i co to mówi o konfiguracji projektu?
- odpowiedź: Od porównania zainstalowanych wersji tu i tam — objaw jest typowy dla dwóch różnych rozwiązań tego samego zakresu, najczęściej w zależności przechodniej. Jeśli okaże się, że CI instaluje z deklaracji, a nie z pliku blokady, to jest przyczyna: deklaracja dopuszcza przedział wersji, a blokada wskazuje jedną, więc bez niej środowiska rozjeżdżają się same z upływem czasu.
- pytanie: Czego plik blokady nie gwarantuje mimo identycznych wersji pakietów?
- odpowiedź: Nie ustala wersji interpretera, bibliotek systemowych ani systemu operacyjnego, więc te elementy trzeba deklarować osobno; nie pomoże też, jeśli potrzebny plik pakietu zostanie wycofany z indeksu.

## Źródła

- [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) — Python Packaging Authority
- [Projects](https://docs.astral.sh/uv/concepts/projects/) — Astral
- [Ruff](https://docs.astral.sh/ruff/) — Astral
