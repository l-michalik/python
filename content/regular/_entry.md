---
rev: 1
fetchedAt: 2026-08-14
refreshedAt: 2026-08-14
---

## Upstream

| komponent | wersja | notatka | url |
| --- | --- | --- | --- |
| CPython | 3.14.7 | Wydanie stabilne z 2026-08-05; pomiary i zachowanie pętli zdarzeń opisane dla gałęzi 3.14. | https://www.python.org/downloads/release/python-3147/ |
| PEP 703 | PEP 703 | Status Final, Python-Version 3.13 — wariant interpretera bez GIL-a wprowadzony do CPythona. | https://peps.python.org/pep-0703/ |
| PEP 779 | PEP 779 | Status Final, Python-Version 3.14 — free-threading z oficjalnym wsparciem, nadal jako osobny wariant kompilacji. | https://peps.python.org/pep-0779/ |
| asyncio | 2026-08-14 | Data stanu strony „Developing with asyncio"; próg `slow_callback_duration` w trybie diagnostycznym wynosi domyślnie 100 ms. | https://docs.python.org/3/library/asyncio-dev.html |
| SQLAlchemy | 2.0.52 | Wydanie z 2026-08-11 wg PyPI; strategie ładowania relacji opisane dla linii 2.0. | https://pypi.org/project/SQLAlchemy/ |
| PostgreSQL 18 | PostgreSQL 18 | Strona `/docs/current/sql-explain.html` rozwiązuje się do wersji 18 — składnia i opcje `EXPLAIN ANALYZE` czytane z tego wydania. | https://www.postgresql.org/docs/current/sql-explain.html |
| mypy | 2.3.0 | Wydanie z 2026-07-13 wg PyPI; dokumentacja protokołów czytana w tej wersji. | https://pypi.org/project/mypy/ |
| coverage | 7.15.4 | Wersja podana w nagłówku dokumentacji Coverage.py w dniu odczytu. | https://coverage.readthedocs.io/en/latest/ |
| pytest | 9.1.1 | Wydanie z 2026-06-19 wg PyPI. | https://pypi.org/project/pytest/ |

## Wymagania

### Produkcyjny kod backendowy w Pythonie

- oferty: 13
- cytaty: „proven track record of developing production-grade applications in Python" (Grid Dynamics); „Strong Python development experience (production systems)" (emagine Polska)
- zagadnienia: pyt-reg-006, pyt-reg-002, pyt-reg-005

### Bazy relacyjne, SQL i praca przez ORM

- oferty: 9
- cytaty: „Comfort with database schema design and performance tuning for real-time and high throughput scenarios" (Shelf); „Proficiency in database development including SQL, PL/SQL, PostgreSQL and Azure SQL" (EPAM Systems)
- zagadnienia: pyt-reg-004

### Budowa REST API w webowym frameworku Pythona

- oferty: 8
- cytaty: „Deep understanding of RESTful API design best practices." (ITDS); „Advanced experience with REST APIs" (DCG)
- pominięte: Warstwa HTTP jest domknięta na poziomie `junior` (pyt-jun-004); to, co na tym poziomie do niej dochodzi — model współbieżności usługi i kontrakt typów na granicy — pokrywają pyt-reg-003 i pyt-reg-006. Utrzymanie API pod ruchem, z SLO i wersjonowaniem, należy do poziomu `advanced` i do skilla `api-design`.

### Testy automatyczne i jakość kodu

- oferty: 8
- cytaty: „Expertise building automated functional testing and CI/CD pipelines using industry standard tools" (EPAM Systems); „Jakość kodu: Dbanie o jakość, czytelność i wydajność kodu oraz udział w przeglądach technicznych." (TSS)
- zagadnienia: pyt-reg-005

### Konteneryzacja i potoki CI/CD

- oferty: 7
- cytaty: „Familiarity with CI/CD pipelines and DevOps tooling (Jenkins, GitHub Actions, GitLab CI)." (ITDS); „Solid hands-on proficiency with Linux environments, Bash/shell scripting, and containerization using Docker." (Grid Dynamics)
- pominięte: Należy do skilli `docker` i `ci-cd`. Część, która jest własnością Pythona — co uruchamiać w potoku i jak czytać wynik tej bramy — pokrywają pyt-reg-005 i pyt-reg-006.

### Wydajność i optymalizacja: wąskie gardła, skalowalność

- oferty: 7
- cytaty: „Optymalizacja: Monitorowanie wydajności procesów przetwarzania danych, identyfikowanie wąskich gardeł oraz wdrażanie usprawnień." (TSS); „Expertise designing applications considering NFRs around high throughput and low latency for data processing" (EPAM Systems)
- zagadnienia: pyt-reg-002, pyt-reg-001, pyt-reg-004

### Integracja modeli językowych w aplikacji produkcyjnej

- oferty: 6
- cytaty: „Hands-on experience developing agentic AI systems, multi-agent architectures, or advanced Retrieval-Augmented Generation (RAG) frameworks." (Grid Dynamics); „Experience building agentic systems: AI agents, tool-calling, orchestration, retrieval, or LLM-backed infrastructure in production" (Shelf)
- pominięte: Należy do skilli `llm`, `rag` i `langchain` — z perspektywy Pythona jest to wywołanie sieciowe o dużym opóźnieniu, czyli przypadek szczególny współbieżności (pyt-reg-003); wszystko, co w tym wymaganiu specyficzne, dotyczy zachowania modelu.

### Diagnostyka produkcyjna i obserwowalność

- oferty: 6
- cytaty: „Troubleshoot and resolve intricate production issues, conducting thorough root-cause analyses." (ITDS); „Practical experience using LangSmith (or equivalent LLMOps platforms) for observability, tracing, debugging, and evaluation of LLM pipelines." (Grid Dynamics)
- zagadnienia: pyt-reg-002, pyt-reg-003, pyt-reg-004

### Praca w chmurze (AWS, Azure, GCP)

- oferty: 6
- cytaty: „Hands-on experience with cloud infrastructure such as AWS, GCP, or Azure" (Shelf); „Knowledge of Cloud technologies such as Azure, Unix/Linux and shell scripting" (EPAM Systems)
- pominięte: Należy do skilli `aws` i `azure` — usługi dostawcy mają własną drabinkę i nie zmieniają się wraz z poziomem znajomości języka.

### Potoki przetwarzania danych: ETL, wsad, integracja źródeł

- oferty: 5
- cytaty: „Design and implement idempotent, restartable batch processing workflows" (emagine Polska); „Showcase of hands-on experience building scalable data pipelines, processing high volume data in batch and stream for near real-time analytics" (EPAM Systems)
- zagadnienia: pyt-reg-007

### Obsługa błędów i odporność na awarie

- oferty: 4
- cytaty: „Implement reconciliation logic across distributed systems" (emagine Polska); „Ensuring data completeness, quality and reconciliation between systems" (DCG)
- zagadnienia: pyt-reg-007

### Współbieżność i przetwarzanie asynchroniczne

- oferty: 3
- cytaty: „Good distributed systems judgment: concurrency, failure handling, data consistency, async work, and service boundaries" (Shelf); „Pracują z kodem wielowątkowym, wieloprocesowym." (CloudFerro)
- zagadnienia: pyt-reg-001, pyt-reg-003

### Algorytmy i struktury danych

- oferty: 3
- cytaty: „Mają dobre podstawy algorytmów i struktur danych." (CloudFerro); „Umiejętność tworzenia oraz optymalizacji zapytań i algorytmów przetwarzających duże zbiory danych." (TSS)
- zagadnienia: pyt-reg-002

### Narzędzia i struktura projektu: zależności, moduły, linter

- oferty: 3
- cytaty: „Familiarity with modern Python tooling (uv, Ruff, Rye), Git workflows." (ITDS); „Follow CI/CD processes with automated checks (ruff, pytest)" (emagine Polska)
- pominięte: Domknięte na poziomie `junior` (pyt-jun-001); to, co dochodzi wyżej, to nie kolejne narzędzie, tylko umiejętność odczytania, ile jego wynik jest wart — i to pokrywają pyt-reg-005 oraz pyt-reg-006.

### Praca z systemem kontroli wersji w zespole

- oferty: 3
- cytaty: „Praca z systemem kontroli wersji Git w modelu zespołowym" (Fabrity); „Familiarity with modern Python tooling (uv, Ruff, Rye), Git workflows." (ITDS)
- pominięte: Należy do skilla `git` — przepływ pracy w repozytorium jest niezależny od języka.

## Changelog

- rev 1 — pierwsze pobranie
