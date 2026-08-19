# joboffers

Projekt ćwiczeniowy do skilla `python` z bazy wiedzy w `content/`. Agregator
ogłoszeń o pracę: pobiera oferty z kilku źródeł HTTP, normalizuje je, zapisuje
do PostgreSQL i wystawia REST API. Do tego potok wsadowy z punktem kontrolnym
i harness pomiarowy.

Domena nie jest przypadkowa — `content/market.md` to próbka trzynastu ogłoszeń
z justjoin.it, a ten projekt przetwarza dokładnie takie dane.

**Repozytorium zawiera szkielet, nie implementację.** Funkcje mają sygnatury,
docstringi z kontraktem i `NotImplementedError`. Testy padają. Lista zadań
i kryteria ukończenia: [TASKS.md](TASKS.md).

## Start

```bash
uv sync                       # środowisko + uv.lock
cp .env.example .env
docker compose up -d          # PostgreSQL 18
uv run pytest -m "not slow and not db"   # zobacz, co pada
```

Skróty w `Makefile`: `make lint type test cov mut bench db api`.

## Układ

```
src/joboffers/
  config.py          ustawienia ze środowiska
  logging_setup.py   JEDYNE miejsce konfiguracji logowania          → T01, T18
  errors.py          hierarchia wyjątków domenowych                 → T02
  domain/            modele i Protocol; bez zależności w dół        → T03, T08
  sources/           wyjście do sieci: sekwencyjnie / wątki / async  → T09, T10
  normalize/         jedyny fragment CPU-bound                      → T03, T12
  storage/           SQLAlchemy: sesja, ORM, repozytorium           → T04, T13
  pipeline/          wsad idempotentny + rekonsyliacja              → T14, T15
  api/               FastAPI                                        → T05
  bench/             harness pomiarowy                              → T11
tests/               testy = kryteria ukończenia
docs/pomiary/        wyniki pomiarów (szablon w SZABLON.md)
docs/decyzje/        krótkie ADR-y
```

## Mapa: zagadnienie → zadanie

| Zagadnienie | Tytuł | Zadanie |
| --- | --- | --- |
| pyt-nic-001 | Po co istnieje Python | T19 |
| pyt-nic-002 | Moduły, pakiety, środowisko wirtualne | T00 |
| pyt-nic-003 | Struktury danych i ich koszt | T03 |
| pyt-nic-004 | Model obiektowy i wyjątki | T02 |
| pyt-nic-005 | Gdzie Python jest właściwą odpowiedzią | T11, T19 |
| pyt-nic-006 | Ekosystem i frameworki | T19 |
| pyt-jun-001 | Środowisko i zależności projektu | T00, T20 |
| pyt-jun-002 | Adnotacje typów i mypy | T07 |
| pyt-jun-003 | Testy jednostkowe w pytest | T06 |
| pyt-jun-004 | REST API w FastAPI | T05 |
| pyt-jun-005 | Dostęp do bazy przez ORM | T04 |
| pyt-jun-006 | Wyjątki, logowanie, traceback | T01, T02, T18 |
| pyt-jun-007 | Współbieżność z gotowych klocków | T09, T11 |
| pyt-reg-001 | GIL i free-threading | **T11** |
| pyt-reg-002 | Profilowanie czasu i pamięci | T12 |
| pyt-reg-003 | asyncio i blokowanie pętli | T10 |
| pyt-reg-004 | N+1 i plan zapytania | T13 |
| pyt-reg-005 | Wartość zestawu testów | T16, T17 |
| pyt-reg-006 | Typowanie strict i protokoły | T08 |
| pyt-reg-007 | Wsad idempotentny i rekonsyliacja | T14, T15 |

## Zasada projektu

Każde zdanie o wydajności, jakości albo poprawności jest zaliczone dopiero
z liczbą. „Jest szybciej" bez pomiaru przed i po nie jest wynikiem.

Dotyczy to również współbieżności: **T11 istnieje po to, żeby udowodnić, kiedy
wątków i procesów dokładać NIE warto.** Domyślną rekomendacją jest
„sekwencyjnie", dopóki pomiar nie pokaże czego innego.
