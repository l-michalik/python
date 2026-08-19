---
id: pyt-reg-007
title: Idempotentne przetwarzanie wsadowe i rekonsyliacja
dependsOn: pyt-jun-007, pyt-jun-005
updated: 2026-08-14
---

## Polecenie

Zaprojektuj potok wsadowy tak, żeby ponowne uruchomienie po awarii nie zdublowało danych, i pokaż, czym mierzysz, że nic nie zginęło.

## Odpowiedź

Idempotencję daje klucz naturalny zdarzenia i zapis warunkowy: rekord wchodzi przez „wstaw albo zaktualizuj" po tym kluczu, więc drugie przetworzenie tej samej porcji nie tworzy duplikatu. Wznawialność daje punkt kontrolny — trwale zapisany znacznik ostatniej ukończonej porcji, aktualizowany w tej samej transakcji co dane. Zgodność mierzy się rekonsyliacją: porównaniem liczby i sumy kontrolnej rekordów po stronie źródła i celu dla tego samego okna czasu.

## Definicja

Operacja idempotentna daje ten sam stan końcowy niezależnie od tego, czy wykonano ją raz, czy wielokrotnie. Punkt kontrolny to zapisany stan postępu pozwalający wznowić pracę od miejsca przerwania zamiast od początku. Rekonsyliacja to porównanie dwóch niezależnych zestawień tych samych danych — źródła i celu — służące do wykrycia rozbieżności, a nie do jej naprawy.

## Zastosowanie

Bierze się to wszędzie tam, gdzie potok działa cyklicznie na danych z zewnątrz, bo awaria w połowie przebiegu jest zdarzeniem oczekiwanym, nie wyjątkowym. emagine Polska wymaga wprost „idempotent, restartable batch processing workflows" oraz „reconciliation logic across distributed systems", DCG „ensuring data completeness, quality and reconciliation between systems", TSS projektowania „procesów ETL/ELT oraz integracji danych z różnych źródeł", EPAM „reliable data pipelines for sourcing, processing, distributing and storing data".

## Jak to działa

Podział na porcje wyznacza jednostkę atomowości: wszystko w porcji wchodzi jedną transakcją razem z aktualizacją punktu kontrolnego, więc po awarii stan jest albo sprzed porcji, albo po niej — nigdy w środku. Klucz idempotencji musi pochodzić z danych źródłowych (identyfikator zdarzenia, para źródło plus przesunięcie), a nie z czasu przetwarzania, bo inaczej ponowne uruchomienie wygeneruje nowy klucz i duplikat. Ponawianie musi być ograniczone: liczba prób, rosnący odstęp między nimi i kolejka rekordów odrzuconych, żeby jeden trwale wadliwy wiersz nie zatrzymywał całego przebiegu w pętli. Rekonsyliacja jest osobnym przebiegiem czytającym oba końce niezależnie — gdyby liczyła po tej samej ścieżce, którą szły dane, potwierdzałaby wyłącznie samą siebie.

## Przykład

Potok ładujący 4,2 mln zdarzeń dziennie porcjami po 10 000:

```
przebieg przerwany po 137 porcjach
wznowienie:      startuje od porcji 138, nie od zera
po zakończeniu:  źródło 4 218 730, cel 4 218 730, różnica 0
przebieg z awarią sieci w porcji 212 i ponowieniem:
                 źródło 4 218 730, cel 4 218 730, duplikatów 0
```

Bez klucza idempotencji drugi przypadek dałby cel 4 228 730, czyli dokładnie jedną porcję nadmiarową — i to jest liczba, po której poznaje się brak zabezpieczenia. Bez punktu kontrolnego pierwszy przypadek oznaczałby ponowne przetworzenie 1,37 mln rekordów, czyli koszt, którego nikt nie mierzy, dopóki nie zacznie przekraczać okna nocnego.

## Ograniczenia

Idempotencja po kluczu chroni przed duplikatem, ale nie przed przetworzeniem tego samego rekordu w dwóch różnych wersjach — do tego potrzebny jest znacznik wersji albo czasu zdarzenia. Punkt kontrolny zapisany poza transakcją danych wprowadza okno, w którym stan i postęp mogą się rozejść. Rekonsyliacja po samej liczbie rekordów przepuszcza uszkodzenie treści, więc do wykrycia zmienionych wartości potrzebna jest suma kontrolna po polach. Przy źródle, które zmienia dane wstecz, porównanie okna czasu przestaje być rozstrzygające.

## Alternatywy

Przetwarzanie strumieniowe z zatwierdzaniem przesunięcia (Kafka) — gdy dane napływają ciągle, a opóźnienie dobowe jest za duże; wymagane przez TSS i EPAM. Pełne przeładowanie zamiast przyrostowego — gdy zbiór jest mały, bo znika wtedy cały problem punktu kontrolnego kosztem czasu przebiegu. Zapis do tabeli tymczasowej i atomowa podmiana — gdy odbiorca nie może zobaczyć stanu pośredniego. Kolejka zadań z gwarancją co najmniej jednego dostarczenia i idempotentnym odbiorcą — gdy porcje są niezależne i mają iść równolegle.

## Typowe błędy

- Klucz idempotencji zbudowany ze znacznika czasu przetwarzania zamiast z identyfikatora zdarzenia — po ponowieniu każdy rekord jest nowy.
- Aktualizacja punktu kontrolnego poza transakcją zapisu danych, czyli okno na rozjazd postępu ze stanem.
- Ponawianie bez ograniczenia liczby prób, przy którym jeden wadliwy rekord blokuje przebieg w nieskończonej pętli.
- Rekonsyliacja licząca po tej samej ścieżce, którą szły dane — potwierdza własne błędy.
- Porównywanie wyłącznie liczby rekordów i uznanie zgodności za dowód poprawności treści.
- Porcja tak duża, że jej transakcja trzyma blokady przez kilkanaście minut i blokuje odczyty.

## Pytania kontrolne

- pytanie: Po awarii sieci potok został ponowiony i w celu jest o 10 000 rekordów więcej niż w źródle. Co to lokalizuje i jaką zmianę wprowadzasz?
- odpowiedź: Nadmiar równy dokładnie jednej porcji lokalizuje problem w idempotencji, nie w punkcie kontrolnym: porcja została zapisana, potwierdzenie nie dotarło, więc ponowienie wstawiło ją drugi raz. Zmianą jest zapis warunkowy po kluczu pochodzącym z danych źródłowych, dzięki któremu powtórzone wstawienie aktualizuje istniejący wiersz zamiast tworzyć nowy — i dopiero wtedy ponawianie jest bezpieczne.
- pytanie: Rekonsyliacja pokazuje zgodne liczby po obu stronach. Dlaczego to jeszcze nie dowodzi, że dane są poprawne?
- odpowiedź: Bo licznik wykrywa braki i duplikaty, a nie zmianę treści — rekord zapisany z uciętym polem albo przeliczony złym kursem nadal jest jednym rekordem. Dowodem jest dopiero porównanie sumy kontrolnej po istotnych polach albo agregatów kwotowych; dodatkowo obie strony trzeba policzyć niezależnymi ścieżkami, bo zestawienie liczone tym samym kodem, który zapisywał, potwierdza własne błędy.
- pytanie: Dlaczego punkt kontrolny musi zostać zapisany w tej samej transakcji co porcja danych?
- odpowiedź: Osobne zapisy tworzą okno awarii, w którym postęp mówi „gotowe", choć danych nie ma, albo dane istnieją bez przesuniętego punktu; jedna transakcja zostawia stan albo sprzed porcji, albo po niej.

## Źródła

- [Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html) — Celery
- [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html) — SQLAlchemy
- [PostgreSQL: EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) — PostgreSQL Global Development Group
