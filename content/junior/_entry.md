---
rev: 1
fetchedAt: 2026-08-14
refreshedAt: 2026-08-14
---

## Upstream

| komponent | wersja | notatka | url |
| --- | --- | --- | --- |
| CPython | 3.14.7 | Wydanie stabilne z 2026-08-05; materiał zakłada składnię i bibliotekę standardową gałęzi 3.14. | https://www.python.org/downloads/release/python-3147/ |
| uv | 0.12.4 | Wydanie z 2026-08-13 wg PyPI — menedżer zależności i plik blokady w zagadnieniu o środowisku. | https://pypi.org/project/uv/ |
| ruff | 0.16.3 | Wydanie z 2026-08-13 wg PyPI — linter i formater konfigurowany w `pyproject.toml`. | https://pypi.org/project/ruff/ |
| pytest | 9.1.1 | Wydanie z 2026-06-19 wg PyPI; wymaga Pythona >=3.10. | https://pypi.org/project/pytest/ |
| mypy | 2.3.0 | Wydanie z 2026-07-13 wg PyPI — dokumentacja czytana w wersji 2.3.0. | https://pypi.org/project/mypy/ |
| fastapi | 0.141.1 | Wydanie z 2026-07-29 wg PyPI. | https://pypi.org/project/fastapi/ |
| SQLAlchemy | 2.0.52 | Wydanie z 2026-08-11 wg PyPI; materiał opisuje API sesji z linii 2.0. | https://pypi.org/project/SQLAlchemy/ |
| PEP 484 | PEP 484 | Status Final, Python-Version 3.5 — adnotacje typów jako metadane, bez egzekwowania w czasie działania. | https://peps.python.org/pep-0484/ |

## Wymagania

### Produkcyjny kod backendowy w Pythonie

- oferty: 13
- cytaty: „Strong proficiency in Python 3.11+ and solid object-oriented programming fundamentals." (ITDS); „Umiejętność pisania czytelnego i utrzymywalnego kodu" (Fabrity)
- zagadnienia: pyt-jun-001, pyt-jun-002, pyt-jun-006

### Bazy relacyjne, SQL i praca przez ORM

- oferty: 9
- cytaty: „Intermediate knowledge of PostgreSQL and SQLAlchemy" (DCG); „Experience with schema design and migrations" (emagine Polska)
- zagadnienia: pyt-jun-005

### Budowa REST API w webowym frameworku Pythona

- oferty: 8
- cytaty: „Build REST APIs using FastAPI" (emagine Polska); „Projektowanie, implementacja i dokumentowanie API (REST) dla aplikacji webowych i mobilnych" (Fabrity)
- zagadnienia: pyt-jun-004

### Testy automatyczne i jakość kodu

- oferty: 8
- cytaty: „Mają doświadczenie w pisaniu testów jednostkowych zgodnie z TDD." (CloudFerro); „Ability to write automated tests, preferably with pytest" (DCG)
- zagadnienia: pyt-jun-003, pyt-jun-001

### Konteneryzacja i potoki CI/CD

- oferty: 7
- cytaty: „Konteneryzacja (Docker) i praca w środowiskach CI/CD" (Fabrity); „Experience with CI/CD and creating deployment pipelines" (DCG)
- pominięte: Należy do skilli `docker` i `ci-cd` — na tym poziomie Python wnosi wyłącznie plik blokady, z którego buduje się obraz, i to jest pokryte przez pyt-jun-001.

### Wydajność i optymalizacja: wąskie gardła, skalowalność

- oferty: 7
- cytaty: „Optymalizacja wydajności aplikacji oraz zapytań do baz danych" (Fabrity); „Comfort with database schema design and performance tuning for real-time and high throughput scenarios" (Shelf)
- pominięte: Poziom `junior` kończy się na sensownych wartościach domyślnych; wskazanie wąskiego gardła wymaga profilu i liczby przed zmianą oraz po niej — poziom `regular`, zagadnienia pyt-reg-002 i pyt-reg-004.

### Integracja modeli językowych w aplikacji produkcyjnej

- oferty: 6
- cytaty: „Practical experience with LLMs at least at an intermediate level" (DCG); „Experience building LLM-powered features or workflows (OpenAI/Anthropic APIs, LangChain, agentic systems)" (comm1t)
- pominięte: Należy do skilli `llm`, `rag` i `langchain` — wywołanie modelu z Pythona jest zwykłym żądaniem HTTP, a treść wymagania dotyczy zachowania modelu, nie języka.

### Diagnostyka produkcyjna i obserwowalność

- oferty: 6
- cytaty: „Monitoring i diagnostyka: Monitorowanie środowisk Big Data, analiza problemów oraz diagnozowanie nieprawidłowości w procesach przetwarzania danych." (TSS); „Debug distributed data inconsistencies" (emagine Polska)
- zagadnienia: pyt-jun-006

### Praca w chmurze (AWS, Azure, GCP)

- oferty: 6
- cytaty: „AWS experience (S3, Glue, Aurora)" (emagine Polska); „Contribute to cloud-based solutions running on AWS and Azure" (Ntiative)
- pominięte: Należy do skilli `aws` i `azure` — usługi dostawcy są osobną drabinką i nie zmieniają się wraz z poziomem znajomości języka.

### Potoki przetwarzania danych: ETL, wsad, integracja źródeł

- oferty: 5
- cytaty: „Design and implement idempotent, restartable batch processing workflows" (emagine Polska); „praca z danymi pochodzącymi z różnych źródeł" (P&P Solutions)
- pominięte: Idempotencja i wznawialność to decyzje o zachowaniu potoku po awarii, a nie złożenie go z gotowych klocków — poziom `regular`, zagadnienie pyt-reg-007.

### Obsługa błędów i odporność na awarie

- oferty: 4
- cytaty: „Obsługa wyjątków, praca z modułami i pakietami" (Fabrity); „Ensuring data completeness, quality and reconciliation between systems" (DCG)
- zagadnienia: pyt-jun-006

### Współbieżność i przetwarzanie asynchroniczne

- oferty: 3
- cytaty: „Doświadczenie w pracy z aplikacjami wielowątkowymi wykorzystującymi bibliotekę Celery, opartymi na systemach kolejkowych (RabbitMQ)" (Fabrity); „Mają doświadczenie w pracy w architekturze opartej na mikroserwisach i asynchronicznych metodach komunikacji (rpc, kolejki)." (CloudFerro)
- zagadnienia: pyt-jun-007

### Algorytmy i struktury danych

- oferty: 3
- cytaty: „Mają dobre podstawy algorytmów i struktur danych." (CloudFerro); „Umiejętność tworzenia oraz optymalizacji zapytań i algorytmów przetwarzających duże zbiory danych." (TSS)
- pominięte: Pokryte na poziomie `nice-to-have` zagadnieniem pyt-nic-003; składanie systemu z gotowych klocków nie zmienia kryterium wyboru struktury, więc osobne zagadnienie na tym poziomie nie miałoby czego dodać. Wraca na poziomie `regular` jako pomiar kosztu pamięciowego (pyt-reg-002).

### Narzędzia i struktura projektu: zależności, moduły, linter

- oferty: 3
- cytaty: „Familiarity with modern Python tooling (uv, Ruff, Rye), Git workflows." (ITDS); „Follow CI/CD processes with automated checks (ruff, pytest)" (emagine Polska)
- zagadnienia: pyt-jun-001

### Praca z systemem kontroli wersji w zespole

- oferty: 3
- cytaty: „Praca z systemem kontroli wersji Git w modelu zespołowym" (Fabrity); „Familiarity with Delta Lake, DLT and GitLab" (EPAM Systems)
- pominięte: Należy do skilla `git` — przepływ pracy w repozytorium jest niezależny od języka i nie ma powodu, żeby drabinka Pythona uczyła go po raz drugi.

## Changelog

- rev 1 — pierwsze pobranie
