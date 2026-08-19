---
id: pyt-jun-006
title: Wyjątki, logowanie i traceback
dependsOn: pyt-nic-004, pyt-nic-001
updated: 2026-08-14
---

## Polecenie

Skonfiguruj logowanie w usłudze tak, żeby po awarii dało się odtworzyć, co się stało, i powiedz, co zapisujesz na każdym poziomie ważności.

## Odpowiedź

Logowanie konfiguruje się raz, w punkcie wejścia programu, a w modułach pobiera się logger po nazwie modułu — wtedy każdy wpis niesie informację, skąd pochodzi. Poziomy dzielą wpisy według tego, kto ma reagować: `DEBUG` dla śledzenia przepływu przy diagnozie, `INFO` dla zdarzeń biznesowych, `WARNING` dla sytuacji obsłużonych, ale nietypowych, `ERROR` dla operacji, która się nie udała, `CRITICAL` dla awarii całej usługi. Wyjątek loguje się razem z tracebackiem, przez `exception` albo `exc_info=True` — bez tego zostaje sam komunikat bez miejsca powstania.

## Definicja

Logger to nazwany punkt zbierania komunikatów; loggery tworzą hierarchię po kropkach w nazwie i dziedziczą konfigurację po rodzicu. Handler decyduje, dokąd wpis trafia (konsola, plik, system zbierania logów), formatter — jak wygląda. Traceback to zapis stosu wywołań od miejsca uruchomienia do miejsca rzucenia wyjątku.

## Zastosowanie

Bierze się to zanim usługa trafi na jakiekolwiek środowisko poza laptopem — log jest jedynym śladem po zdarzeniu, którego nikt nie oglądał na żywo. Sześć ogłoszeń w próbce mówi o diagnostyce: ITDS o „root-cause analyses", Shelf o „reliability, observability, performance, and incident follow-through", TSS o „analizie problemów oraz diagnozowaniu nieprawidłowości", emagine o „Debug distributed data inconsistencies".

## Jak to działa

Wpis przechodzi dwa filtry: poziom loggera i poziom handlera — komunikat poniżej któregokolwiek z nich znika bez śladu. Po przejściu jest przekazywany w górę hierarchii do handlerów rodziców, aż do loggera głównego, chyba że propagacja została wyłączona. Argumenty formatujące podaje się jako parametry (`logger.info("zapisano %s", klucz)`), a nie sklejone łańcuchy — dzięki temu formatowanie wykonuje się dopiero wtedy, gdy wpis faktycznie ma być zapisany. Wywołanie `logger.exception` wewnątrz bloku `except` dokłada aktualny traceback, bo sięga po wyjątek obsługiwany w tym momencie.

## Przykład

```python
import logging

logger = logging.getLogger(__name__)

def przetworz(dokument_id: str) -> None:
    try:
        zapisz(dokument_id)
    except OSError:
        logger.exception("zapis dokumentu %s nie powiódł się", dokument_id)
        raise
```

Trzy rzeczy naraz: `exception` zapisuje traceback, identyfikator dokumentu wchodzi jako parametr (więc da się po nim szukać w zbieranych logach), a `raise` bez argumentu przekazuje ten sam wyjątek dalej z nienaruszonym stosem. Bez `raise` warstwa wyżej dostałaby ciszę i uznała, że zapis się udał.

## Ograniczenia

Log jest tak dobry, jak wpisy, które ktoś przewidział — nie zastąpi metryk ani śladu rozproszonego, bo nie pokazuje czasu spędzonego w każdym etapie ani powiązania żądań między usługami. Nadmiar wpisów na poziomie `DEBUG` na produkcji kosztuje wydajność i pieniądze za składowanie, a jednocześnie topi sygnał w szumie. Logi łatwo zamieniają się w wyciek danych: wpis z całym ciałem żądania wynosi hasła i dane osobowe do systemu, w którym siedzą latami.

## Alternatywy

`print` — wyłącznie w skrypcie jednorazowym, bo nie ma poziomów, znacznika czasu ani miejsca pochodzenia. Logowanie strukturalne (structlog, format JSON) — gdy wpisy trafiają do systemu, w którym się je przeszukuje po polach, a nie czyta okiem. Ślad rozproszony (OpenTelemetry, wymagany przez ITDS) — gdy pytanie brzmi „gdzie poszedł czas", a nie „co się stało". Kryterium: log do zdarzeń, ślad do czasu, metryka do liczby.

## Typowe błędy

- Konfiguracja logowania wywoływana w module bibliotecznym zamiast w punkcie wejścia — nadpisuje ustawienia aplikacji, która tę bibliotekę wciągnęła.
- `logger.error(str(e))` zamiast `logger.exception` — zostaje komunikat bez tracebacku, czyli bez informacji, gdzie to powstało.
- Sklejanie wartości w komunikat (`f"zapisano {klucz}"`), przez co każdy wpis jest unikalnym łańcuchem i nie da się ich pogrupować.
- Logowanie i ponowne rzucanie tego samego wyjątku na każdej warstwie — jedna awaria daje pięć wpisów wyglądających jak pięć awarii.
- Wpisywanie do logu całych ciał żądań razem z danymi uwierzytelniającymi.

## Pytania kontrolne

- pytanie: Po awarii masz w logu wyłącznie linię „zapis nie powiódł się" i żadnego stosu. Co zmieniasz w kodzie i dlaczego to wystarczy do wskazania przyczyny?
- odpowiedź: Zamieniam `logger.error` na `logger.exception` w bloku `except` — ta funkcja dokłada traceback aktualnie obsługiwanego wyjątku, czyli pełną ścieżkę wywołań i typ błędu. Sam komunikat mówi tylko, że wybrana gałąź się wykonała; stos mówi, która operacja i w którym pliku zawiodła, więc dopiero on odróżnia brak uprawnień od nieistniejącej ścieżki.
- pytanie: Zespół ustawił na produkcji poziom `DEBUG`, żeby „mieć więcej informacji". Jakie są tego koszty i co proponujesz zamiast?
- odpowiedź: Koszt jest potrójny: formatowanie i zapis wpisów obciążają usługę, składowanie kosztuje, a istotne wpisy toną w szumie, więc diagnostyka staje się wolniejsza, nie szybsza. Zamiast tego trzymam `INFO` jako domyślny i włączam `DEBUG` punktowo dla wybranego loggera na czas diagnozy — hierarchia loggerów po nazwie modułu pozwala zawęzić to do jednego komponentu.
- pytanie: Dlaczego wpisy z pełnym ciałem żądania są ryzykiem nawet, gdy pomagają w diagnozie?
- odpowiedź: Mogą zawierać hasła i dane osobowe, które po zapisaniu trafiają do systemu logów na lata; do diagnozy zapisuje się minimalny bezpieczny kontekst i maskuje dane wrażliwe.

## Źródła

- [logging — Logging facility for Python](https://docs.python.org/3/library/logging.html) — Python Software Foundation
- [8. Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) — Python Software Foundation
- [The Python Standard Library](https://docs.python.org/3/library/index.html) — Python Software Foundation
