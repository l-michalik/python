---
id: pyt-nic-002
title: Moduły, pakiety i środowisko wirtualne
updated: 2026-08-14
---

## Polecenie

Opisz, gdzie fizycznie mieszka kod, który importujesz, i po co projekt dostaje własne środowisko.

## Odpowiedź

Import nie szuka kodu „w projekcie", tylko przechodzi listę katalogów `sys.path` i bierze pierwszy pasujący moduł. Środowisko wirtualne to osobny katalog z własnym interpreterem i własnym zestawem zainstalowanych pakietów, wstawiany na początek tej listy — dzięki temu dwa projekty mogą wymagać dwóch niezgodnych wersji tej samej biblioteki i żaden nie psuje drugiego ani systemowego Pythona.

## Definicja

Moduł to pojedynczy plik `.py`, którego przestrzeń nazw można wciągnąć do innego pliku instrukcją `import`. Pakiet to katalog grupujący moduły, rozpoznawany po tym, że da się go zaimportować jako całość. Środowisko wirtualne (`venv`) to katalog zawierający dowiązanie do interpretera i katalog `site-packages`, w którym lądują zależności zainstalowane wyłącznie dla tego projektu.

## Zastosowanie

Podział na moduły bierze się do rozdzielenia odpowiedzialności w rosnącym kodzie: warstwa dostępu do bazy, warstwa API i logika domenowa w osobnych plikach dają się testować i podmieniać osobno. Środowisko wirtualne bierze się natychmiast po utworzeniu projektu — ogłoszenie Fabrity wymaga wprost „pracy z modułami i pakietami", a ITDS „modern Python tooling", i obie te rzeczy zaczynają się od tego, że projekt ma własny, odtwarzalny zestaw zależności.

## Jak to działa

Przy `import x` interpreter najpierw sprawdza `sys.modules` — słownik już wczytanych modułów; trafienie kończy sprawę, więc drugi import tego samego modułu nie wykonuje jego kodu ponownie. Przy chybieniu przechodzi po kolei katalogi z `sys.path`: katalog uruchamianego skryptu, potem katalogi środowiska. Pierwszy pasujący plik wygrywa. Aktywacja środowiska wirtualnego sprowadza się do ustawienia zmiennych powłoki tak, żeby `python` wskazywał na interpreter z tego katalogu, a jego `site-packages` stało w `sys.path` przed pakietami systemowymi.

## Przykład

```
projekt/
  .venv/                  # środowisko: interpreter + site-packages
  pyproject.toml          # deklaracja zależności
  app/
    __init__.py
    api.py
    baza.py
  tests/
    test_api.py
```

W `api.py` zapis `from app.baza import polacz` działa, bo katalog `projekt/` jest w `sys.path`. Plik `random.py` położony obok `api.py` przesłoniłby bibliotekę standardową o tej samej nazwie — pierwszy pasujący wpis w `sys.path` wygrywa i nikt nie zgłosi ostrzeżenia.

## Ograniczenia

Środowisko wirtualne izoluje pakiety Pythona, ale nie izoluje wersji samego interpretera (dostajesz tę, z której środowisko utworzono), nie izoluje bibliotek systemowych, od których zależą pakiety binarne, i nie jest granicą bezpieczeństwa — kod z pakietu ma pełny dostęp do systemu plików. Nie jest też mechanizmem odtwarzalności: samo `.venv` nie mówi, jakie wersje zainstalowano, dopóki nie ma pliku, który to zapisuje.

## Alternatywy

Do izolacji całego systemu operacyjnego, a nie tylko pakietów — kontener Docker; wymagają go DCG, Fabrity i Grid Dynamics. Do równoległego trzymania wielu wersji interpretera — menedżer wersji (`pyenv`, `uv python`). Do środowisk z pakietami binarnymi spoza PyPI — conda. Kryterium: `venv` wystarcza, dopóki różnice między projektami są w pakietach Pythona; gdy różnią się bibliotekami systemowymi albo wersją Pythona, potrzebna jest warstwa niżej.

## Typowe błędy

- Instalowanie zależności globalnie, bo „to tylko jeden pakiet" — pierwszy konflikt wersji ujawnia się w innym projekcie i wygląda jak jego błąd.
- Nazwanie własnego pliku tak jak moduł z biblioteki standardowej (`random.py`, `types.py`, `logging.py`) i późniejsze szukanie, dlaczego zniknęła funkcja z tamtego modułu.
- Wrzucenie katalogu `.venv` do repozytorium — waży setki megabajtów, jest niemigrowalny między systemami i tak nie zastępuje deklaracji zależności.
- Uznanie, że aktywowane środowisko obowiązuje w innym oknie terminala albo w zadaniu CI.

## Pytania kontrolne

- pytanie: Kolega uruchamia ten sam kod co ty i dostaje `ImportError` na bibliotece, którą ty masz zainstalowaną. Gdzie szukasz przyczyny?
- odpowiedź: W tym, że biblioteka siedzi w twoim środowisku, a nie w deklaracji zależności projektu — u ciebie import znajduje ją w `site-packages`, u niego tego wpisu w `sys.path` nie ma. Sprawdza się to porównaniem listy zainstalowanych pakietów, a naprawia dopisaniem zależności do pliku projektu, nie ręczną instalacją u kolegi.
- pytanie: Po co projektowi osobne środowisko, skoro system ma już zainstalowanego Pythona?
- odpowiedź: Bo dwa projekty prędzej czy później zażądają dwóch niezgodnych wersji tej samej biblioteki, a jeden globalny `site-packages` mieści tylko jedną. Środowisko daje każdemu projektowi własny katalog pakietów wstawiany przed systemowy, więc instalacja w jednym nie zmienia zachowania drugiego ani narzędzi systemu.
- pytanie: Dlaczego po zmianie środowiska ten sam import może załadować inny moduł?
- odpowiedź: Import bierze pierwszy pasujący moduł z `sys.path`, a środowisko wirtualne zmienia kolejność katalogów i własne `site-packages`; trzeba sprawdzić ścieżkę załadowanego modułu, nie zakładać jego pochodzenia po nazwie.

## Źródła

- [6. Modules](https://docs.python.org/3/tutorial/modules.html) — Python Software Foundation
- [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html) — Python Software Foundation
- [Managing Application Dependencies](https://packaging.python.org/en/latest/tutorials/managing-dependencies/) — Python Packaging Authority
