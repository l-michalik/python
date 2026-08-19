---
id: pyt-jun-004
title: REST API w FastAPI
dependsOn: pyt-nic-006, pyt-nic-001
updated: 2026-08-14
---

## Polecenie

Wystaw endpoint przyjmujący dane w ciele żądania i pokaż, w którym miejscu odrzucane jest niepoprawne wejście.

## Odpowiedź

Trasę deklaruje się dekoratorem na funkcji (`@app.post("/zamowienia")`), a kształt ciała żądania — klasą modelu z adnotacjami typów. Framework sam czyta JSON, sprawdza go względem modelu i odrzuca niezgodne żądanie odpowiedzią 422, zanim twoja funkcja w ogóle zostanie wywołana. To samo źródło — adnotacje modelu — generuje schemat OpenAPI, więc dokumentacja nie jest osobnym plikiem do utrzymania.

## Definicja

REST API to interfejs, w którym zasoby mają adresy, a operacje wyraża się metodami HTTP. FastAPI to framework webowy budujący warstwę HTTP na adnotacjach typów: model Pydantic opisuje ciało żądania i odpowiedzi, a schemat OpenAPI powstaje z niego automatycznie. Walidacja w czasie działania jest tu tym, czego same adnotacje z poprzedniego zagadnienia nie dają — sprawdzeniem danych przychodzących z zewnątrz.

## Zastosowanie

Bierze się to do usług, które są API dla innych usług lub dla aplikacji mobilnej, i wszędzie tam, gdzie kontrakt musi być spisany. W próbce rynkowej budowa REST API wystąpiła w ośmiu ogłoszeniach na trzynaście: ITDS mówi o „RESTful API design best practices", emagine o „Build REST APIs using FastAPI", Fabrity o „projektowaniu, implementacji i dokumentowaniu API (REST)".

## Jak to działa

Przy starcie framework przechodzi wszystkie zarejestrowane funkcje, odczytuje ich adnotacje i buduje z nich dwie rzeczy: walidator dla każdego parametru oraz schemat OpenAPI. Przy żądaniu dopasowuje ścieżkę do trasy, wyciąga parametry ze ścieżki, z zapytania i z ciała, przepuszcza je przez walidator i dopiero wynik podaje do twojej funkcji już jako obiekty właściwych typów. Niezgodność kończy się odpowiedzią 422 z listą pól, które nie przeszły — twój kod się nie wykonuje. Ten sam mechanizm w drugą stronę serializuje zwrócony obiekt do JSON według modelu odpowiedzi, obcinając pola, których w nim nie ma.

## Przykład

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Zamowienie(BaseModel):
    produkt: str = Field(min_length=1, max_length=200)
    sztuk: int = Field(gt=0, le=1000)

@app.post("/zamowienia", status_code=201)
def utworz(zamowienie: Zamowienie) -> dict[str, int]:
    return {"sztuk": zamowienie.sztuk}
```

Żądanie z `"sztuk": 0` dostanie 422 i nie wejdzie do funkcji, bo `gt=0` jest częścią kontraktu, a nie sprawdzeniem w ciele. Granice `le=1000` i `max_length=200` nie są ozdobą: bez nich pojedyncze żądanie może zamówić miliard sztuk albo wcisnąć megabajt tekstu do kolumny bazy.

## Ograniczenia

Framework waliduje kształt danych, nie ich sens — poprawny typowo identyfikator produktu, którego nie ma w bazie, przejdzie walidację i wybuchnie warstwę niżej. Nie załatwia też uwierzytelniania, ograniczania liczby żądań ani transakcji; to warstwy do dołożenia. Funkcja trasy zadeklarowana jako `def`, a nie `async def`, jest uruchamiana w puli wątków — pomylenie tych dwóch trybów zmienia model współbieżności całej usługi, co jest tematem poziomu wyżej.

## Alternatywy

Django z Django REST Framework — gdy projekt potrzebuje też panelu administracyjnego, ORM-a i szablonów z jednego pudełka; ITDS i Fabrity trzymają obie opcje obok siebie. Flask — gdy tras jest kilka i nie potrzeba walidacji ani schematu. gRPC — gdy klientem jest inna usługa, liczy się rozmiar i szybkość, a przeglądarka nie jest odbiorcą. Kryterium: FastAPI, gdy kontrakt jest publiczny i musi być udokumentowany.

## Typowe błędy

- Walidacja przepisana ręcznie w ciele funkcji, mimo że model potrafi ją wyrazić deklaratywnie — dwa źródła prawdy, z których jedno nie trafia do dokumentacji.
- Zwracanie modelu bazy danych wprost jako odpowiedzi, przez co pola wewnętrzne (hasło, identyfikatory obce) wyciekają do klienta.
- Brak górnych granic na polach liczbowych i tekstowych, czyli otwarte zaproszenie do żądania, które wysyci pamięć.
- Zwracanie 200 na utworzenie zasobu i sygnalizowanie błędów w treści odpowiedzi zamiast kodem statusu.

## Pytania kontrolne

- pytanie: Klient zgłasza, że jego żądanie „nie działa", i dostaje 422 z listą pól. Czy to błąd twojej usługi i skąd wiesz?
- odpowiedź: Nie — 422 znaczy, że żądanie nie przeszło walidacji kontraktu, więc kod trasy w ogóle się nie wykonał, a lista pól w odpowiedzi wskazuje, które nie spełniły ograniczeń modelu. Błędem usługi byłoby to dopiero wtedy, gdyby kontrakt w schemacie OpenAPI opisywał coś innego niż faktyczny model, więc weryfikuję zgodność jednego z drugim, zanim zacznę zmieniać kod.
- pytanie: Skąd biorą się wartości `gt=0` i `le=1000` w modelu zamówienia i co się zmieni, jeśli je usuniesz?
- odpowiedź: Z granic sensu domenowego i z ochrony zasobów: zero sztuk nie jest zamówieniem, a górna granica ustawia sufit na to, co pojedyncze żądanie może zarezerwować. Po ich usunięciu walidacja przepuści zero i wartości skrajnie duże, więc sprawdzenie przeniesie się do logiki albo do bazy — a tam objawi się wyjątkiem lub uszkodzonymi danymi zamiast czytelnej odpowiedzi 422.
- pytanie: Dlaczego model odpowiedzi FastAPI chroni kontrakt, a nie tylko dokumentuje endpoint?
- odpowiedź: Framework serializuje wynik według modelu i usuwa pola, których kontrakt nie przewiduje, więc przypadkowe dane z obiektu wewnętrznego nie wyciekną do klienta.

## Źródła

- [Request Body](https://fastapi.tiangolo.com/tutorial/body/) — FastAPI
- [fastapi — PyPI](https://pypi.org/project/fastapi/) — Python Package Index
- [typing — Support for type hints](https://docs.python.org/3/library/typing.html) — Python Software Foundation
