---
rev: 1
fetchedAt: 2026-08-14
refreshedAt: 2026-08-14
---

## Upstream

| komponent | wersja | notatka | url |
| --- | --- | --- | --- |
| CPython | 3.14.7 | Wydanie stabilne z 2026-08-05. Gałęzie 3.14 i 3.13 w statusie bugfix, 3.12–3.10 wyłącznie security, 3.15 w przedwydaniu. | https://www.python.org/downloads/release/python-3147/ |
| PEP 20 | PEP 20 | Status Active, typ Informational — zasady projektowe języka, bez numeru wydania. | https://peps.python.org/pep-0020/ |
| PEP 779 | PEP 779 | Status Final, Python-Version 3.14 — od tej wersji interpreter bez GIL-a ma status oficjalnie wspieranego, ale nie domyślnego. | https://peps.python.org/pep-0779/ |
| The Python Standard Library | 2026-08-14 | Data stanu strony spisu biblioteki standardowej; stopka podaje „Last updated on Aug 14, 2026 (07:55 UTC)". | https://docs.python.org/3/library/index.html |
| fastapi | 0.141.1 | Wydanie z 2026-07-29 wg PyPI — framework porównywany w zagadnieniu o ekosystemie. | https://pypi.org/project/fastapi/ |

## Wymagania

### Produkcyjny kod backendowy w Pythonie

- oferty: 13
- cytaty: „Piszą czytelny i wydajny kod w Pythonie." (CloudFerro); „Strong Python skills and the ability to design clean, maintainable backend code" (Shelf)
- zagadnienia: pyt-nic-001, pyt-nic-004, pyt-nic-005

### Bazy relacyjne, SQL i praca przez ORM

- oferty: 9
- cytaty: „Knowledge of relational databases, especially PostgreSQL." (ITDS); „Znajomość relacyjnych baz danych oraz pracy z ORM" (Fabrity)
- pominięte: Wymaga uruchomienia zapytania i pracy z sesją ORM, czyli złożenia działającego systemu z gotowych klocków — poziom `junior`, zagadnienie pyt-jun-005.

### Budowa REST API w webowym frameworku Pythona

- oferty: 8
- cytaty: „Deep understanding of RESTful API design best practices." (ITDS); „Bardzo dobra znajomość Django / FastAPI" (Fabrity)
- zagadnienia: pyt-nic-006

### Testy automatyczne i jakość kodu

- oferty: 8
- cytaty: „Mają doświadczenie w pisaniu testów jednostkowych zgodnie z TDD." (CloudFerro); „Ability to write automated tests, preferably with pytest" (DCG)
- pominięte: Testu, którego się nie uruchomiło, nie da się zaliczyć z definicji poziomu — wymaganie domyka uruchomiony zestaw na poziomie `junior` (pyt-jun-003) i pomiar jego wartości na poziomie `regular` (pyt-reg-005).

### Konteneryzacja i potoki CI/CD

- oferty: 7
- cytaty: „Konteneryzacja (Docker) i praca w środowiskach CI/CD" (Fabrity); „Familiarity with CI/CD pipelines and DevOps tooling (Jenkins, GitHub Actions, GitLab CI)." (ITDS)
- pominięte: Należy do skilli `docker` i `ci-cd` — środowisko uruchomieniowe i automatyzacja wydania nie są własnością języka.

### Wydajność i optymalizacja: wąskie gardła, skalowalność

- oferty: 7
- cytaty: „Optymalizacja: Monitorowanie wydajności procesów przetwarzania danych, identyfikowanie wąskich gardeł oraz wdrażanie usprawnień." (TSS); „Expertise designing applications considering NFRs around high throughput and low latency for data processing" (EPAM Systems)
- pominięte: Wymaga zobaczenia pomiaru przed zmianą i po niej, czego na poziomie rozpoznawania pojęć zaliczyć się nie da — poziom `regular`, zagadnienia pyt-reg-001 i pyt-reg-002.

### Integracja modeli językowych w aplikacji produkcyjnej

- oferty: 6
- cytaty: „Experience with LLMs in production (OCR, content processing, enrichment)" (emagine Polska); „Doświadczenie w integracji rozwiązań opartych na sztucznej inteligencji (AI)" (Fabrity)
- pominięte: Należy do skilli `llm`, `rag` i `langchain` — Python jest tu warstwą wywołania, a wymaganie dotyczy zachowania modelu, nie języka.

### Diagnostyka produkcyjna i obserwowalność

- oferty: 6
- cytaty: „Troubleshoot and resolve intricate production issues, conducting thorough root-cause analyses." (ITDS); „Own services after launch: reliability, observability, performance, and incident follow-through" (Shelf)
- pominięte: Część językowa — wyjątki, traceback, logowanie — idzie na poziom `junior` (pyt-jun-006); analiza przyczyny źródłowej pod ruchem wymaga systemu na produkcji, czyli poziomu `advanced` i skilla `observability`.

### Praca w chmurze (AWS, Azure, GCP)

- oferty: 6
- cytaty: „Hands-on experience with cloud infrastructure such as AWS, GCP, or Azure" (Shelf); „Has experience with cloud platforms such as AWS, Azure, or GCP" (Ntiative)
- pominięte: Należy do skilli `aws` i `azure` — dostawca infrastruktury jest osią niezależną od języka.

### Potoki przetwarzania danych: ETL, wsad, integracja źródeł

- oferty: 5
- cytaty: „Experience with data pipelines (ETL / batch processing)" (emagine Polska); „ETL/ELT: Doświadczenie w projektowaniu i rozwijaniu procesów ETL/ELT oraz integracji danych z różnych źródeł." (TSS)
- pominięte: Wymaga wznawialności i uzgadniania stanu po awarii, czyli decyzji popartych zachowaniem działającego potoku — poziom `regular`, zagadnienie pyt-reg-007.

### Obsługa błędów i odporność na awarie

- oferty: 4
- cytaty: „Obsługa wyjątków, praca z modułami i pakietami" (Fabrity); „Good distributed systems judgment: concurrency, failure handling, data consistency, async work, and service boundaries" (Shelf)
- zagadnienia: pyt-nic-004

### Współbieżność i przetwarzanie asynchroniczne

- oferty: 3
- cytaty: „Pracują z kodem wielowątkowym, wieloprocesowym." (CloudFerro); „Doświadczenie w pracy z aplikacjami wielowątkowymi wykorzystującymi bibliotekę Celery, opartymi na systemach kolejkowych (RabbitMQ)" (Fabrity)
- zagadnienia: pyt-nic-005

### Algorytmy i struktury danych

- oferty: 3
- cytaty: „Mają dobre podstawy algorytmów i struktur danych." (CloudFerro); „Has solid understanding of software architecture, algorithms, and data structures" (Ntiative)
- zagadnienia: pyt-nic-003

### Narzędzia i struktura projektu: zależności, moduły, linter

- oferty: 3
- cytaty: „Familiarity with modern Python tooling (uv, Ruff, Rye), Git workflows." (ITDS); „Obsługa wyjątków, praca z modułami i pakietami" (Fabrity)
- zagadnienia: pyt-nic-002

### Praca z systemem kontroli wersji w zespole

- oferty: 3
- cytaty: „Praca z systemem kontroli wersji Git w modelu zespołowym" (Fabrity); „Familiarity with modern Python tooling (uv, Ruff, Rye), Git workflows." (ITDS)
- pominięte: Należy do skilla `git` — przepływ pracy w repozytorium jest niezależny od języka.

## Changelog

- rev 1 — pierwsze pobranie
