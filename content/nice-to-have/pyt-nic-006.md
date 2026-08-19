---
id: pyt-nic-006
title: Ekosystem: biblioteka standardowa, PyPI, frameworki
updated: 2026-08-14
---

## Polecenie

Naszkicuj mapę ekosystemu Pythona i powiedz, po czym poznajesz, że do zadania trzeba sięgnąć poza bibliotekę standardową.

## Odpowiedź

Biblioteka standardowa jedzie z interpreterem i pokrywa podstawy: pliki, sieć na niskim poziomie, formaty danych, testy, logowanie, współbieżność. PyPI to publiczne repozytorium reszty — kilkuset tysięcy pakietów, z których w ogłoszeniach powtarzają się trzy rodziny: frameworki webowe (Django, FastAPI, Flask), dostęp do danych (SQLAlchemy, pandas, Spark) i warstwa AI (LangChain, biblioteki dostawców modeli). Po bibliotekę zewnętrzną sięgasz wtedy, gdy zadanie jest standardowym problemem branży, a nie właściwością twojej domeny.

## Definicja

Biblioteka standardowa to zestaw modułów instalowanych razem z interpreterem, wersjonowany razem z nim. PyPI (Python Package Index) to publiczne repozytorium pakietów instalowanych przez menedżer zależności. Framework webowy to biblioteka narzucająca strukturę aplikacji — przyjmuje żądanie HTTP, kieruje je do twojej funkcji i zamienia jej wynik na odpowiedź.

## Zastosowanie

Mapa ekosystemu jest potrzebna, żeby czytać ogłoszenia: w próbce rynkowej tej bazy Django lub FastAPI występuje w pięciu ofertach, PostgreSQL z ORM w sześciu, a warstwa LLM w sześciu. Bez tej mapy tech-stack ogłoszenia jest listą nazw; z nią widać, że to trzy warstwy tej samej aplikacji — wejście HTTP, trwałe dane, model.

## Jak to działa

Instalacja pakietu sprowadza pliki z PyPI do katalogu `site-packages` bieżącego środowiska, razem z jego własnymi zależnościami, i wtedy staje się on zwykłym modułem do zaimportowania. Framework webowy odwraca kierunek wywołań: to nie twój kod woła bibliotekę, tylko framework woła twoją funkcję, gdy przyjdzie pasujące żądanie. Django niesie ze sobą komplet — ORM, panel administracyjny, warstwę szablonów — i narzuca układ projektu. FastAPI i Flask dają samą warstwę HTTP, a bazę, walidację i resztę dobiera się osobno.

## Przykład

Ta sama funkcjonalność „przyjmij dane i zapisz" w dwóch podejściach: w Django model, migracja i widok są częścią jednego frameworka i piszesz je jego konwencjami; w FastAPI deklarujesz funkcję, dokładasz walidację przez Pydantic i osobno SQLAlchemy do zapisu. Pierwsze podejście jest szybsze na starcie i sztywniejsze, drugie wymaga złożenia klocków, ale pozwala podmienić każdy z nich. Ogłoszenia w próbce trzymają obie kolumny naraz — ITDS i Fabrity wymieniają „Django/FastAPI" jednym tchem.

## Ograniczenia

Zależność zewnętrzna to cudzy kod z własnym tempem wydawania, własnymi lukami bezpieczeństwa i własnymi zależnościami; każda dołożona biblioteka zwiększa powierzchnię, którą trzeba aktualizować. Biblioteka standardowa nie ma tego problemu, ale wydaje się razem z Pythonem, więc poprawki docierają wolniej. Popularność pakietu nie jest gwarancją utrzymania — sprawdza się datę ostatniego wydania i liczbę otwartych zgłoszeń, nie liczbę gwiazdek.

## Alternatywy

Do warstwy HTTP: Django, gdy zakres jest typowym CRUD-em z panelem administracyjnym; FastAPI, gdy usługa jest API dla innych usług i liczy się walidacja oraz dokumentacja OpenAPI; Flask, gdy potrzebna jest cienka warstwa nad kilkoma trasami. Do danych: SQLAlchemy przy bazie relacyjnej, pandas przy zbiorze mieszczącym się w pamięci, Spark przy zbiorze, który się nie mieści. Do zadań w tle: Celery przy kolejce zadań, harmonogram systemowy przy jednym zadaniu na dobę.

## Typowe błędy

- Instalowanie biblioteki do zadania, które biblioteka standardowa pokrywa jednym modułem (parsowanie dat, JSON, ścieżki).
- Wybór frameworka po popularności, a nie po kształcie projektu — Django pod czyste API jest ciężki, FastAPI pod aplikację z panelem administracyjnym oznacza dopisywanie tego, co Django ma.
- Mylenie nazwy z rolą: pandas i Spark nie są alternatywą dla PostgreSQL, tylko warstwą przetwarzania nad danymi, które gdzieś muszą leżeć.
- Dobieranie biblioteki bez sprawdzenia, czy jest utrzymywana i z jakimi wersjami Pythona współpracuje.

## Pytania kontrolne

- pytanie: Zespół zaczyna usługę, która ma wystawić kilkanaście endpointów dla aplikacji mobilnej i nie potrzebuje żadnego interfejsu webowego. Django czy FastAPI, i co przesądza?
- odpowiedź: FastAPI — wartość Django leży w warstwach, których ta usługa nie użyje: szablonach i panelu administracyjnym, a jego ORM i układ projektu trzeba by przyjąć w komplecie. FastAPI daje samą warstwę HTTP z walidacją i dokumentacją OpenAPI, więc bazę i resztę klocków dobiera się do potrzeby. Gdyby jednak w zakresie pojawił się panel dla redakcji, rachunek odwraca się na korzyść Django.
- pytanie: Po czym poznajesz, że zadanie należy oddać bibliotece zewnętrznej, zamiast pisać je samemu?
- odpowiedź: Po tym, że problem jest standardowy dla branży, a nie właściwością twojej domeny — parsowanie formatu, protokół, dostęp do bazy. Własna implementacja takiej rzeczy powtarza cudze błędy i wymaga utrzymania; z drugiej strony każda zależność to kod, który trzeba aktualizować, więc do rzeczy, którą biblioteka standardowa robi jednym modułem, nie dokłada się pakietu.
- pytanie: Dlaczego sama popularność pakietu nie wystarcza do jego wyboru?
- odpowiedź: Liczba gwiazdek nie mówi, czy pakiet jest utrzymywany ani czy ma aktualne poprawki bezpieczeństwa; sprawdza się datę ostatniego wydania, otwarte zgłoszenia i koszt aktualizowania zależności.

## Źródła

- [The Python Standard Library](https://docs.python.org/3/library/index.html) — Python Software Foundation
- [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) — Python Packaging Authority
- [Request Body](https://fastapi.tiangolo.com/tutorial/body/) — FastAPI
