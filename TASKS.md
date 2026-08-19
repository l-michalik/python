# Zadania — projekt `joboffers`

Lista zadań do wykonania **przez Ciebie**. Repozytorium zawiera szkielet:
sygnatury, kontrakty (`Protocol`), konfigurację narzędzi i **testy, które na
starcie padają**. Test przechodzący = zadanie zaliczone, o ile spełnione są też
pozostałe punkty definicji ukończenia (dalej: **DoD**).

Zasada obowiązująca w całym projekcie: **każde zdanie o wydajności, jakości albo
poprawności jest zaliczone dopiero z liczbą.** „Jest szybciej" bez pomiaru przed
i po nie jest wynikiem, tylko deklaracją. Wyniki pomiarów lądują w
`docs/pomiary/` wg szablonu `docs/pomiary/SZABLON.md`.

Kolumna „Zagadnienia" wskazuje pliki w `content/`, z których zadanie wynika.

---

## Kolejność

Zadania są ułożone tak, że kolejne opiera się na poprzednim — to jest ten sam
porządek, co `dependsOn` w bazie wiedzy.

```
T00 ── T01 ── T02 ── T03 ── T04 ── T05 ── T06 ── T07 ── T08
                      │      │      │             └─ T16 ── T17
                      │      └─ T13 ┘
                      └─ T09 ── T10 ── T11 ── T12
                                        └─ T14 ── T15
T18, T19, T20 — w dowolnym momencie po T06
```

---

## T00 — Środowisko odtwarzalne u kogoś innego

**Zagadnienia:** pyt-jun-001, pyt-nic-002
**Pliki:** `pyproject.toml`, `uv.lock`, `.env`, `docker-compose.yml`

**Po co.** Zanim napiszesz pierwszą linię logiki, projekt musi się odtwarzać
identycznie na innej maszynie. Deklaracja mówi „czego potrzebuję", plik blokady
mówi „co u mnie zadziałało" — do repozytorium wchodzą oba.

**Kroki**

1. `uv sync` — wygeneruj `uv.lock` i zatwierdź go osobnym commitem.
2. Skopiuj `.env.example` do `.env`, uzupełnij, sprawdź że `.env` jest w `.gitignore`.
3. `docker compose up -d`, sprawdź `pg_isready`.
4. Uzupełnij `src/joboffers/cli.py` tak, żeby `uv run joboffers fetch` startowało
   i kończyło się czytelnym komunikatem, a nie tracebackiem.

**DoD**

- [ ] `uv.lock` w repozytorium; `uv sync --frozen` przechodzi na czystym klonie.
- [ ] `uv run ruff check .` — zero zgłoszeń.
- [ ] `uv run joboffers --help` wypisuje pomoc i kończy się kodem 0.
- [ ] Umiesz odpowiedzieć, **czego plik blokady nie gwarantuje** (trzy rzeczy) — zapisz to w `docs/decyzje/T00.md`.
- [ ] Górne granice wersji w `pyproject.toml` mają uzasadnienie w komentarzu (dlaczego `<3.0` dla SQLAlchemy).

**Pułapka.** Przypięcie wszystkiego na sztywno w `pyproject.toml` zamiast w
blokadzie — blokuje poprawki bezpieczeństwa i nic nie wnosi.

---

## T01 — System logowania w całym projekcie

**Zagadnienia:** pyt-jun-006
**Pliki:** `src/joboffers/logging_setup.py`, wszystkie moduły
**Test:** `tests/test_logging_setup.py`

**Po co.** Log jest jedynym śladem po zdarzeniu, którego nikt nie oglądał na
żywo. Konfiguracja rozproszona po modułach oznacza, że biblioteka nadpisuje
ustawienia aplikacji, która ją wciągnęła.

**Kroki**

1. Zaimplementuj `configure_logging(level, fmt)` — idempotentne, wołane
   **wyłącznie** z punktów wejścia (`cli.py`, `api/app.py`, `tests/conftest.py`).
2. W każdym module: `logger = logging.getLogger(__name__)`. Zero `print`
   (reguła `T20` w ruff to wymusza).
3. Formatter `json` obok `text` — wpis ma nieść `timestamp`, `level`, `logger`,
   `message`, `run_id`.
4. Zaimplementuj `RequestIdFilter` dokładający `run_id` do każdego rekordu.
5. Przejdź przez wszystkie moduły i ustaw poziomy: `DEBUG` = przepływ,
   `INFO` = zdarzenie biznesowe, `WARNING` = obsłużone, ale nietypowe,
   `ERROR` = operacja nieudana, `CRITICAL` = usługa nie działa.

**DoD**

- [ ] `tests/test_logging_setup.py` przechodzi w całości.
- [ ] `grep -rn "print(" src/joboffers | grep -v bench | grep -v cli.py` — pusty wynik.
- [ ] `grep -rn 'logger\.\(info\|warning\|error\|debug\)(f"' src/` — pusty wynik (żadnych f-stringów w logach).
- [ ] Każde `logger.exception` znajduje się wewnątrz `except`; każde `logger.error` bez `exc_info` ma uzasadnienie w komentarzu.
- [ ] Wywołanie `configure_logging()` dwa razy nie duplikuje handlerów (pokrywa test).
- [ ] Wpisy z tego samego przebiegu da się wyfiltrować po jednym polu `run_id`.

**Pułapka.** `logger.error(str(e))` zamiast `logger.exception` — zostaje
komunikat bez informacji, gdzie to powstało.

---

## T02 — Hierarchia wyjątków i przepływ błędu przez warstwy

**Zagadnienia:** pyt-nic-004, pyt-jun-006
**Pliki:** `src/joboffers/errors.py`, wszystkie warstwy

**Po co.** Kod błędu zwracany jako wartość da się zignorować; wyjątek nie.
Wspólny przodek pozwala wywołującemu złapać całą rodzinę albo jeden przypadek.

**Kroki**

1. Ustal, która warstwa **łapie** wyjątek, a która tylko przepuszcza. Zapisz to
   jako trzy zdania w `docs/decyzje/T02.md`.
2. Zamień wszystkie surowe `raise ValueError(...)` na wyjątki z `errors.py`.
3. Wprowadź regułę: wyjątek loguje się **raz**, na granicy, na której zapada
   decyzja o obsłudze — nie na każdej warstwie po drodze.
4. W FastAPI podepnij handler zamieniający `JobOffersError` na odpowiedź HTTP
   z właściwym kodem (nie 500 dla wszystkiego).

**DoD**

- [ ] Żaden moduł poza `errors.py` nie definiuje własnej klasy wyjątku bez przodka `JobOffersError`.
- [ ] Jedna awaria pobrania daje **dokładnie jeden** wpis `ERROR` w logu — sprawdź to, wymuszając awarię w `FakeOfferSource(failure_rate=1.0)` i licząc wpisy.
- [ ] `except Exception:` występuje maksymalnie w jednym miejscu (najwyższa pętla przebiegu) i ma komentarz z uzasadnieniem.
- [ ] Test: żądanie na nieistniejącą ofertę zwraca 404, a nie 500.

**Pułapka.** Logowanie i ponowne rzucanie tego samego wyjątku na każdej warstwie
— jedna awaria wygląda w logu jak pięć.

---

## T03 — Normalizacja i wybór struktury danych

**Zagadnienia:** pyt-nic-003, pyt-nic-004
**Pliki:** `src/joboffers/normalize/text.py`, `src/joboffers/domain/models.py`
**Testy:** `tests/test_domain_models.py`, `tests/test_normalize.py`

**Po co.** Wybór struktury jest pierwszą decyzją wydajnościową i zapada zanim
ktokolwiek pomyśli o profilerze. Ten moduł jest też jedynym CPU-bound
fragmentem projektu — wróci w T11 i T12.

**Kroki**

1. Zaimplementuj `clean_text`, `parse_seniority`, `normalize`, `normalize_many`.
2. `deduplicate` napisz **najpierw naiwnie** — `if offer in wynik` na liście.
3. Zmierz oba warianty na 10 000 i 100 000 ofert (`timeit`, seria powtórzeń).
4. Popraw na wariant oparty na zbiorze / słowniku i zmierz ponownie.
5. Zapisz cztery liczby do `docs/pomiary/T03-deduplikacja.md`.

**DoD**

- [ ] `tests/test_domain_models.py` i `tests/test_normalize.py` przechodzą.
- [ ] W `docs/pomiary/T03-deduplikacja.md` są **cztery** liczby (2 warianty × 2 rozmiary) i zdanie, jak rośnie czas względem N w każdym z nich.
- [ ] Umiesz uzasadnić, dlaczego `Offer` musi być `frozen`, żeby wariant docelowy w ogóle był możliwy.
- [ ] `normalize_many` na 1000 rekordach, z których 3 są wadliwe, zwraca 997 ofert i loguje 3 wpisy `WARNING` — nie przerywa się.
- [ ] `fingerprint` jest stabilny między uruchomieniami procesu (uwaga na `hash()` i `PYTHONHASHSEED`).

**Pułapka.** Użycie wbudowanego `hash()` do `fingerprint` — jest solony per
proces, więc rekonsyliacja w T15 przestanie działać między przebiegami.

---

## T04 — Warstwa danych: ORM, sesja, migracje

**Zagadnienia:** pyt-jun-005
**Pliki:** `src/joboffers/storage/db.py`, `orm.py`, `repository.py`, `alembic/`

**Po co.** Granica transakcji i cykl życia sesji to dwie rzeczy, które decydują
o tym, czy usługa przetrwa pod obciążeniem.

**Kroki**

1. `make_engine`, `make_session_factory`, `session_scope` — commit na wyjściu,
   rollback na wyjątku.
2. `alembic init alembic`, podłącz `Base.metadata`, wygeneruj pierwszą migrację,
   uruchom ją, **przeczytaj wygenerowany plik** i popraw, co trzeba.
3. Zaimplementuj `count` i `list_offers` (na razie wersja naiwna, z leniwym
   ładowaniem — to jest materiał do T13).
4. Napisz test integracyjny z markerem `db`.

**DoD**

- [ ] `alembic upgrade head` na pustej bazie tworzy komplet tabel; `alembic downgrade base` je usuwa.
- [ ] Migracja jest w repozytorium i ma opisową nazwę.
- [ ] `pytest -m db` przechodzi przy uruchomionym `docker compose`.
- [ ] Sesja żyje **na żądanie / na porcję**, nie na proces — pokaż to, sprawdzając liczbę zajętych połączeń w puli podczas 50 równoczesnych żądań.
- [ ] Umiesz odpowiedzieć na pytanie: zapis bez `commit`, potem zapytanie w tej samej sesji — czy zobaczy rekord i czy rekord jest zapisany. (To dwa różne pytania.)

**Pułapka.** `commit` w pętli po każdym rekordzie przy ładowaniu tysięcy wierszy.

---

## T05 — REST API w FastAPI

**Zagadnienia:** pyt-jun-004
**Pliki:** `src/joboffers/api/app.py`, `schemas.py`
**Test:** `tests/test_api.py`

**Kroki**

1. Zaimplementuj `POST /offers` i `GET /offers`.
2. Model odpowiedzi **osobny** od modelu ORM.
3. Paginacja po kursorze, nie po `OFFSET`.
4. Obejrzyj `/docs` i porównaj wygenerowany schemat OpenAPI z tym, co faktycznie
   przyjmuje endpoint.

**DoD**

- [ ] `tests/test_api.py` przechodzi (bez testu z markerem `db`).
- [ ] Każde pole liczbowe i tekstowe w `schemas.py` ma **górną** granicę.
- [ ] Odpowiedź nie zawiera żadnego pola, którego nie ma w `OfferOut` — udowodnij testem, nie przeglądem.
- [ ] Utworzenie zasobu zwraca 201, nie 200.
- [ ] Zero ręcznej walidacji w ciele funkcji trasy — wszystko deklaratywnie w modelu.

**Pułapka.** Zwracanie modelu ORM wprost — pola wewnętrzne wyciekają do klienta.

---

## T06 — Zestaw testów jednostkowych

**Zagadnienia:** pyt-jun-003
**Pliki:** `tests/`

**Kroki**

1. Uzupełnij `FakeOfferSource` — atrapa bez sieci, ze sterowalnym opóźnieniem
   i awaryjnością.
2. Do każdej funkcji z `normalize/text.py` dopisz parametryzację obejmującą
   **granice dziedziny**, nie losowe wartości.
3. Sprawdź zakresy fixture: co ma być `function`, a co może być `session`.

**DoD**

- [ ] `pytest -m "not slow and not db"` — zielono, czas poniżej 5 s.
- [ ] `pytest -p no:randomly` i `pytest` w losowej kolejności dają ten sam wynik (brak przeciekającego stanu).
- [ ] Żaden test nie jest bez asercji.
- [ ] Porównania liczb zmiennoprzecinkowych przez `pytest.approx`, nie `==`.
- [ ] Dla każdego zestawu parametrów umiesz powiedzieć **dlaczego ta wartość** (granica, przypadek pusty, wartość skrajna).

**Pułapka.** Fixture o zakresie `session` trzymająca stan mutowalny — kolejność
testów zaczyna mieć znaczenie.

---

## T07 — Adnotacje typów i mypy (zasięg, nie liczba błędów)

**Zagadnienia:** pyt-jun-002
**Pliki:** wszystkie

**Po co.** mypy domyślnie **pomija funkcje bez sygnatur**. Zero błędów na
projekcie bez adnotacji nie znaczy „czysto", tylko „nie ma czego czytać".

**Kroki**

1. Uruchom `uv run mypy` i zapisz liczbę zgłoszeń — to punkt odniesienia.
2. Zmierz **zasięg**: ile funkcji ma adnotacje. Najprościej: włącz
   `disallow_untyped_defs` na jednym module i policz nowe zgłoszenia.
3. Uzupełniaj sygnatury moduł po module, zaczynając od granic (`domain`,
   `protocols`, publiczne funkcje warstw).
4. Każde `# type: ignore` musi mieć **kod błędu** (`# type: ignore[arg-type]`)
   i komentarz.

**DoD**

- [ ] `uv run mypy` — zero zgłoszeń.
- [ ] `grep -rn "type: ignore" src/ | grep -v "\[" ` — pusty wynik (żadnych wyciszeń bez kodu).
- [ ] `grep -rcn ": Any" src/` — liczba znana, każde wystąpienie uzasadnione w komentarzu.
- [ ] W `docs/pomiary/T07-typy.md`: odsetek funkcji z adnotacjami przed i po.
- [ ] Rozumiesz, dlaczego funkcja z sygnaturą `-> int` może zwrócić `None` i program nie wybuchnie.

**Pułapka.** Traktowanie liczby błędów mypy jako miary jakości bez sprawdzenia,
jaki odsetek kodu jest w ogóle analizowany.

---

## T08 — Tryb strict i `Protocol`

**Zagadnienia:** pyt-reg-006
**Pliki:** `pyproject.toml` (sekcje `[[tool.mypy.overrides]]`), `domain/protocols.py`

**Po co.** Włączenie `strict` globalnie na całym repozytorium kończy się
wyłączeniem go tydzień później. Włącza się modułami.

**Kroki**

1. `domain.*` jest już w `strict` — doprowadź go do zera zgłoszeń.
2. Dokładaj kolejne moduły do `overrides` **po jednym**: `normalize`, `storage`,
   `sources`, `pipeline`, `api`. Po każdym: zero zgłoszeń przed dodaniem następnego.
3. Sprawdź, czy implementacje faktycznie spełniają `Protocol` — dodaj do testów
   asercję przypisania (`_: OfferRepository = SqlOfferRepository(session)`).
4. Zamknij granicę z bibliotekami bez informacji o typach jawnie w
   `pyproject.toml`, nie komentarzami rozsypanymi po plikach.

**DoD**

- [ ] `strict = true` obowiązuje dla **co najmniej pięciu** modułów, jawnie wypisanych w `pyproject.toml`.
- [ ] `uv run mypy` — zero zgłoszeń.
- [ ] `domain/` nie importuje niczego z `storage`, `sources`, `api` — sprawdź `grep`.
- [ ] W `docs/decyzje/T08.md`: dlaczego `Protocol`, a nie wspólna klasa bazowa (odpowiedź ma dotyczyć kierunku zależności, nie stylu).
- [ ] Liczba `# type: ignore` i `Any` na granicach jest zapisana — to jest realny zasięg sprawdzenia.

---

## T09 — Współbieżne pobieranie: wątki

**Zagadnienia:** pyt-jun-007
**Pliki:** `src/joboffers/sources/http_source.py`
**Test:** `tests/test_sources.py`

**Kroki**

1. Zaimplementuj `fetch_one` z limitem czasu, ograniczoną liczbą ponowień
   i rosnącym odstępem.
2. `fetch` (sekwencyjnie) i `fetch_threaded` (`ThreadPoolExecutor`) — **identyczny
   wynik**, różny sposób wykonania.
3. Ustal `max_workers` liczbą, nie na oko: sprawdź limit równoczesnych żądań
   źródła i rozmiar puli połączeń.

**DoD**

- [ ] Testy `test_sources.py` (poza `slow`) przechodzą.
- [ ] `fetch(urls) == fetch_threaded(urls)` dla 100 adresów — pokrywa test.
- [ ] Awaria jednego adresu nie przerywa pobrania pozostałych; zwrócony wynik mówi, których adresów zabrakło.
- [ ] Wartość `max_workers` ma uzasadnienie w komentarzu wskazujące **limit po drugiej stronie**, nie liczbę rdzeni.
- [ ] Żaden obiekt mutowalny nie jest współdzielony między wątkami bez synchronizacji — przejdź kod i wypisz w `docs/decyzje/T09.md`, co jest współdzielone.

**Pułapka.** Dobranie puli **procesów** do zadania czekającego na sieć.

---

## T10 — Wariant asynchroniczny i wykrycie blokowania pętli

**Zagadnienia:** pyt-reg-003
**Pliki:** `src/joboffers/sources/http_source.py`, `src/joboffers/api/app.py`

**Kroki**

1. `fetch_async` na `httpx.AsyncClient` + `asyncio.gather` **z semaforem**.
2. Uruchom z `asyncio.run(main(), debug=True)` i zobacz ostrzeżenia o wywołaniach
   przekraczających `slow_callback_duration` (domyślnie 100 ms).
3. **Celowo** wstaw do trasy `async def` wywołanie synchroniczne (np.
   `time.sleep(0.3)` albo synchroniczne zapytanie do bazy). Zmierz p95 przy 1,
   10 i 50 równoczesnych żądaniach.
4. Napraw przez `asyncio.to_thread` (albo asynchroniczny sterownik) i zmierz ponownie.

**DoD**

- [ ] W `docs/pomiary/T10-petla.md`: p95 przed i po, dla 1 / 10 / 50 równoczesnych żądań.
- [ ] Umiesz pokazać w logu **konkretne ostrzeżenie** trybu diagnostycznego wskazujące blokującą funkcję.
- [ ] `gather` nigdzie nie jest wołany bez ograniczenia równoległości.
- [ ] Każde zadanie utworzone przez `create_task` ma trzymaną referencję.
- [ ] Rozumiesz i umiesz uzasadnić: dlaczego samo przepisanie na `async` nie przyspieszyło niczego, dopóki sterownik pod spodem był synchroniczny.

**Pułapka.** Wypchnięcie **pętli liczącej** do `to_thread` i uznanie jej za
zrównolegloną — GIL zostaje.

---

## T11 — POMIAR: czy wątki albo procesy w ogóle pomogą

**Zagadnienia:** pyt-reg-001, pyt-nic-005, pyt-jun-007
**Pliki:** `src/joboffers/bench/harness.py`, `workloads.py`, `concurrency.py`
**Test:** `tests/test_bench_concurrency.py`

**Po co.** To jest zadanie, które ma udowodnić, że **współbieżność bywa
szkodliwa**. Wynik ma rozstrzygać spór liczbą, zanim ktokolwiek przepisze
produkcyjny moduł. Trzy z pięciu przypadków poniżej powinny skończyć się
rekomendacją „zostaw sekwencyjnie".

**Kroki**

1. Zaimplementuj `io_bound`, `cpu_bound`, `mixed_bound` — dobierz `n` tak, żeby
   **czas sekwencyjny był podobny** dla wszystkich trzech.
2. Zaimplementuj `run_sequential`, `run_threads`, `run_processes`, `run_asyncio`.
3. `repeat` — seria powtórzeń, odczyt odporny na szum (pojedynczy przebieg mierzy
   głównie stan pamięci podręcznej).
4. **Uwaga na pułapkę pomiarową:** `time.process_time()` nie liczy czasu procesów
   potomnych. Dla `ProcessPoolExecutor` dołóż
   `resource.getrusage(RUSAGE_CHILDREN)`, inaczej wariant procesowy pokaże
   `cpu/wall ≈ 0` i wyjdzie na „darmowy".
5. Uruchom pełną macierz: 3 obciążenia × 4 modele × `workers ∈ {1,2,4,8,16}`.
6. Zmierz **osobno** koszt samego startu puli procesów i koszt serializacji
   argumentów (ten sam pomiar dla `items` o rozmiarze 1 KB i 10 MB).
7. Zaimplementuj `decide()` — funkcję zamieniającą odczyty na rekomendację.
8. Napisz raport `docs/pomiary/T11-wspolbieznosc.md`.

**DoD**

- [ ] Testy `test_bench_concurrency.py` przechodzą, łącznie z oznaczonymi `slow`.
- [ ] Raport zawiera tabelę z kolumnami: obciążenie, model, `workers`, `wall_s`, `cpu_s`, `cpu/wall`, przyspieszenie względem sekwencyjnego.
- [ ] Raport pokazuje **przypadek pogorszenia** — konfigurację, w której współbieżność jest wolniejsza od sekwencyjnej. Podaj o ile procent i dlaczego.
- [ ] Dla `cpu_bound` na wątkach: `cpu/wall ≈ 1` przy 4 i 8 wątkach — z komentarzem, że to jest podpis GIL-a.
- [ ] Dla `io_bound` na wątkach: `wall_s` maleje ~liniowo, `cpu_s` stoi.
- [ ] Podany jest **próg opłacalności procesów**: przy jakim rozmiarze argumentu zysk z równoległości znika w koszcie serializacji. Jedna liczba w bajtach lub w rekordach.
- [ ] `decide()` zwraca `"sekwencyjnie"` dla obciążenia, na którym najlepszy wariant poprawia czas o mniej niż 10% — i jest to udokumentowane jako **domyślna rekomendacja**, a nie przypadek brzegowy.
- [ ] Odpowiedź na pytanie z liczbą: czy `normalize_many` z T03 warto zrównoleglić? Jeśli tak — na wątkach czy na procesach i od jakiej liczby ofert.
- [ ] Raport wymienia, czego pomiar **nie** rozstrzyga (inna maszyna, inna liczba rdzeni, biblioteki natywne zwalniające GIL).

**Pułapka #1.** Mierzenie samym czasem ściennym — nie widać różnicy między
„równolegle" a „na zmianę".
**Pułapka #2.** Obciążenie zabawkowe mieszczące się w pamięci podręcznej
procesora i przeniesienie wniosku na dane produkcyjne.
**Pułapka #3.** Użycie NumPy w `cpu_bound` — biblioteka natywna zwalnia GIL,
więc pomiar pokaże równoległość, której Twoja pętla nie ma.

---

## T12 — Profilowanie czasu i pamięci

**Zagadnienia:** pyt-reg-002
**Pliki:** `src/joboffers/normalize/text.py`

**Kroki**

1. Wygeneruj 500 000 sztucznych rekordów i uruchom `normalize_many` pod
   `cProfile`; posortuj po **czasie własnym** (`tottime`), nie skumulowanym.
2. Zapisz ranking dziesięciu pozycji — to jest punkt odniesienia.
3. Znajdź pracę powtarzaną w pętli (kompilacja wyrażenia regularnego, budowa
   obiektu, konwersja) i wynieś ją poza pętlę.
4. Porównaj warianty przez `timeit` (seria, nie pojedynczy przebieg).
5. `tracemalloc`: zestaw dwie migawki i wskaż trzy linie alokujące najwięcej.
   Sprawdź, czy zamiana listy na generator zbija szczyt zużycia pamięci.

**DoD**

- [ ] `docs/pomiary/T12-profil.md` zawiera ranking **przed** i **po**, z tego samego wejścia i tym samym sposobem pomiaru.
- [ ] Podany jest udział procentowy dominującej pozycji przed zmianą i po.
- [ ] Podana jest **górna granica zysku** dla pozycji, której świadomie NIE optymalizowałeś (np. „zapis to 6% czasu, więc maksymalny zysk to 6%").
- [ ] Szczyt zużycia pamięci przed i po zmianie na generator — dwie liczby w MB.
- [ ] `tracemalloc` nie zostaje włączony na stałe w kodzie produkcyjnym.

**Pułapka.** Optymalizowanie funkcji o najwyższym czasie **skumulowanym** — na
szczycie tej kolumny zawsze stoi wywołanie główne.

---

## T13 — N+1 i plan zapytania

**Zagadnienia:** pyt-reg-004
**Pliki:** `src/joboffers/storage/repository.py`, `src/joboffers/api/app.py`

**Kroki**

1. Załaduj do bazy co najmniej 100 000 ofert z tagami (skrypt w `scripts/`).
2. Podepnij licznik zapytań: `event.listen(engine, "before_cursor_execute", ...)`.
   Policz zapytania na **jedno** żądanie `GET /offers?limit=100`.
3. Napraw przez `selectinload`. Zmierz ponownie.
4. Porównaj z `joinedload` — zmierz **rozmiar wyniku**, nie tylko liczbę zapytań.
5. Zostaw jedno zapytanie wolne (filtr po kolumnie bez indeksu) i uruchom na nim
   `EXPLAIN ANALYZE`. Dodaj indeks, uruchom ponownie.
6. Odblokuj test `test_liczba_zapytan_widoku_listy_jest_stala_wzgledem_limitu`.

**DoD**

- [ ] `docs/pomiary/T13-orm.md`: liczba zapytań i czas dla `limit ∈ {10, 100, 1000}` przed i po.
- [ ] Po poprawce liczba zapytań jest **stała** względem `limit`.
- [ ] Porównanie `selectinload` vs `joinedload`: liczba zapytań, liczba wierszy zwróconych przez bazę, czas. Wskazana rekomendacja z uzasadnieniem.
- [ ] Wklejony plan `EXPLAIN ANALYZE` przed i po dodaniu indeksu, z zaznaczonym `Seq Scan` → `Index Scan`.
- [ ] Zapisana rozbieżność między szacowaną a faktyczną liczbą wierszy w planie, z interpretacją.
- [ ] Test odblokowany i przechodzi.
- [ ] Pomiar wykonany na bazie o rozmiarze produkcyjnym, nie na tysiącu wierszy — zapisz liczbę rekordów.

**Pułapka.** Zamiana wszystkich relacji na ładowanie zachłanne „na wszelki
wypadek" — problem N+1 zamienia się w przesyłanie danych, których nikt nie użyje.

---

## T14 — Idempotentny, wznawialny potok wsadowy

**Zagadnienia:** pyt-reg-007
**Pliki:** `src/joboffers/pipeline/batch.py`, `storage/repository.py`
**Test:** `tests/test_pipeline_batch.py`

**Kroki**

1. `chunked` jako generator.
2. `upsert_many` — zapis warunkowy po `dedup_key`, jedna instrukcja na porcję.
3. `run_batch` z punktem kontrolnym zapisywanym **w tej samej transakcji** co
   dane porcji.
4. Ograniczone ponawianie: liczba prób, rosnący odstęp, kolejka odrzuconych.
5. Wymuś awarię w połowie przebiegu (`kill -9` albo wyjątek po N porcjach)
   i uruchom ponownie.

**DoD**

- [ ] Testy `test_pipeline_batch.py` przechodzą (te z markerem `db` przy uruchomionej bazie).
- [ ] Dwa pełne przebiegi na tym samym wejściu dają w celu **tyle samo** rekordów — liczba w raporcie.
- [ ] Po awarii po porcji 137 wznowienie startuje od 138 — pokaż wpis w logu i wartość `checkpoints.batch_no`.
- [ ] Jeden trwale wadliwy rekord **nie** blokuje przebiegu; trafia do kolejki odrzuconych, która jest przeglądalna.
- [ ] Klucz idempotencji pochodzi z danych źródłowych — udowodnij testem, że przebieg uruchomiony dzień później nie tworzy duplikatów.
- [ ] Rozmiar porcji ma uzasadnienie: zmierz czas trzymania blokad dla `batch_size ∈ {1 000, 10 000, 100 000}` i wybierz.

**Pułapka.** Punkt kontrolny zapisany **poza** transakcją danych — okno, w którym
postęp mówi „gotowe", choć danych nie ma.

---

## T15 — Rekonsyliacja

**Zagadnienia:** pyt-reg-007
**Pliki:** `src/joboffers/pipeline/reconcile.py`, `normalize/text.py`

**Kroki**

1. `fingerprint` po polach istotnych, stabilny między procesami.
2. `checksum_window` po stronie celu — liczone **SQL-em**, niezależną ścieżką.
3. Strona źródła liczona z surowych rekordów, **nie** przez ten sam kod, który
   zapisywał.
4. `is_consistent` — zgodne muszą być liczniki **i** sumy kontrolne.
5. Wymuś rozbieżność: ucięcie pola tekstowego przy zapisie. Sprawdź, że
   porównanie samych liczników jej **nie** wykrywa, a suma kontrolna wykrywa.

**DoD**

- [ ] Raport rekonsyliacji dla pełnego przebiegu: liczba źródło, liczba cel, suma źródło, suma cel, różnica.
- [ ] Udokumentowany eksperyment, w którym liczniki są równe, a dane uszkodzone — z pokazaniem, że suma kontrolna to wyłapuje.
- [ ] Obie strony liczone niezależnymi ścieżkami — opisz w `docs/decyzje/T15.md`, na czym polega ta niezależność.
- [ ] Rekonsyliacja da się uruchomić dla dowolnego okna czasu z linii poleceń.
- [ ] Umiesz nazwać przypadek, którego rekonsyliacja po oknie czasu **nie** rozstrzygnie (źródło zmieniające dane wstecz).

---

## T16 — Ile wart jest zestaw testów

**Zagadnienia:** pyt-reg-005
**Pliki:** `tests/`, `pyproject.toml`

**Kroki**

1. `pytest --cov` z `branch = true` (już włączone). Zapisz pokrycie linii **i**
   gałęzi — porównaj obie liczby.
2. `mutmut run --paths-to-mutate src/joboffers/normalize`. Zapisz odsetek zabitych.
3. Przejrzyj ocalałe mutanty. **Odsiej równoważne** — te, których żaden test nie
   może zabić, bo nie zmieniają zachowania.
4. Dopisz testy zabijające pozostałe. Zwróć uwagę na warunki graniczne (`>` vs `>=`).
5. Uruchom mutacje ponownie.

**DoD**

- [ ] `docs/pomiary/T16-testy.md`: pokrycie linii, pokrycie gałęzi, odsetek zabitych mutantów — przed i po.
- [ ] Różnica między pokryciem linii a gałęzi jest wyjaśniona jednym zdaniem odnoszącym się do konkretnego warunku w kodzie.
- [ ] Lista ocalałych mutantów z podziałem na „równoważne" i „brak testu" — z uzasadnieniem dla każdego równoważnego.
- [ ] Co najmniej jeden nowy test wynikający wprost z ocalałego mutanta, na warunku granicznym.
- [ ] Mutacje uruchamiane **punktowo** na module krytycznym, nie na całym repozytorium przy każdym scaleniu — zapisz czas obu wariantów jako uzasadnienie.

**Pułapka.** Ustawienie progu pokrycia linii w CI i uznanie sprawy za zamkniętą
— próg spełnia się też testami bez asercji.

---

## T17 — Test regresji wydajności

**Zagadnienia:** pyt-reg-005, pyt-reg-004
**Pliki:** `tests/test_regresja_wydajnosci.py` (do napisania)

**Po co.** Zmiana z dwóch zapytań na dwieście przechodzi przegląd kodu, bo testy
poprawności są zielone. Bramę trzeba postawić na liczbie.

**Kroki**

1. Zapisz punkt odniesienia: liczba zapytań `GET /offers?limit=100`, czas
   `normalize_many` na 10 000 rekordów, szczyt pamięci potoku wsadowego.
2. Napisz testy porównujące bieżący pomiar z zapisanym punktem odniesienia
   z tolerancją.
3. Uzasadnij tolerancję — za wąska daje testy migoczące, za szeroka nie łapie nic.

**DoD**

- [ ] Test **liczby zapytań** (nie czasu) na widoku listy — pada, gdy ktoś usunie `selectinload`. Sprawdź, usuwając go celowo.
- [ ] Test czasu z tolerancją i z uzasadnieniem tej tolerancji w komentarzu.
- [ ] Punkt odniesienia jest w repozytorium jako plik, nie jako liczba wklejona w asercji.
- [ ] Testy oznaczone markerem `slow`, uruchamiane w CI, ale nie w pętli TDD.
- [ ] Uruchomienie 10 razy z rzędu daje 10 zielonych wyników (test nie migocze).

---

## T18 — Bezpieczne logi

**Zagadnienia:** pyt-jun-006
**Pliki:** `src/joboffers/logging_setup.py`

**Kroki**

1. Zaimplementuj `redact` — działające także zagnieżdżone, niewrażliwe na
   wielkość liter.
2. Przejdź wszystkie miejsca, w których loguje się dane wejściowe. Zamień pełne
   ciała na minimalny bezpieczny kontekst.
3. Sprawdź, czy nagłówek `Authorization` nie trafia do logu przy błędzie HTTP.

**DoD**

- [ ] Testy maskowania przechodzą, łącznie z przypadkiem zagnieżdżonym.
- [ ] Żaden wpis nie zawiera pełnego ciała żądania — przejrzyj log z pełnego przebiegu i potwierdź.
- [ ] Wyjątek z biblioteki HTTP nie wynosi nagłówków do logu (sprawdź, wymuszając 401).
- [ ] `DEBUG` nie jest domyślnym poziomem na żadnym środowisku poza lokalnym.
- [ ] Umiesz wskazać, jak włączyć `DEBUG` **punktowo** dla jednego modułu bez zmiany globalnego poziomu.

---

## T19 — Decyzja architektoniczna: FastAPI czy Django

**Zagadnienia:** pyt-nic-006, pyt-nic-001, pyt-nic-005
**Pliki:** `docs/decyzje/T19-framework.md`

**Po co.** To jest pytanie zadawane na rozmowie i pytanie projektowe. Odpowiedź
„bo lubię FastAPI" nie jest odpowiedzią.

**DoD**

- [ ] Dokument w formacie ADR: kontekst, rozważane opcje, decyzja, konsekwencje.
- [ ] Co najmniej trzy kryteria rozstrzygające, każde odniesione do **tego** projektu (nie do abstrakcyjnego).
- [ ] Wskazany warunek, przy którym decyzja byłaby odwrotna.
- [ ] Osobna sekcja: która część systemu **nie powinna** być w Pythonie i jaka liczba z T11 to uzasadnia.
- [ ] Dokument mieści się na jednej stronie.

---

## T20 — Brama jakości w CI

**Zagadnienia:** pyt-jun-001, pyt-reg-005, pyt-reg-006
**Pliki:** `.github/workflows/ci.yml` (do napisania)

**Kroki**

1. Potok: `uv sync --frozen` → `ruff check` → `ruff format --check` → `mypy` →
   `pytest -m "not slow"` z pokryciem → osobny etap `slow` + `db` z usługą Postgres.
2. Instalacja **z pliku blokady**, nie z deklaracji.

**DoD**

- [ ] Potok przechodzi na czystym klonie.
- [ ] Instalacja z `--frozen` — celowo zepsuj blokadę i sprawdź, że CI pada.
- [ ] Progi jakości są jawne: pokrycie gałęzi, zero zgłoszeń mypy, zero zgłoszeń ruff.
- [ ] Testy `db` mają usługę Postgres w potoku i faktycznie się uruchamiają (nie są cicho pomijane) — sprawdź licznik testów w logu.
- [ ] Czas pełnego potoku zmierzony i zapisany; jeśli przekracza 10 minut, wskazany etap do rozdzielenia.

---

## Podsumowanie kryteriów przekrojowych

Niezależnie od zadania, zaliczone jest tylko to, co spełnia wszystkie poniższe:

| Kryterium | Sprawdzenie |
| --- | --- |
| Kod przechodzi bramę | `make lint type test` — zielono |
| Zmiana wydajności ma dwie liczby | wpis w `docs/pomiary/` wg szablonu |
| Decyzja projektowa ma uzasadnienie | wpis w `docs/decyzje/` |
| Nowe zachowanie ma test | test pada przed zmianą, przechodzi po |
| Log niesie kontekst | `run_id` obecny, dane wrażliwe zamaskowane |
| Typy opisują kontrakt | moduł w `strict`, zero `Any` bez komentarza |
