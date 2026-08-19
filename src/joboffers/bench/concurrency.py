"""Porownanie modeli wykonania: sekwencyjnie / watki / procesy / asyncio.

Zagadnienia: pyt-reg-001, pyt-jun-007, pyt-nic-005, pyt-reg-003.

To jest kod stojacy za zadaniem T11. Wynik ma odpowiedziec na pytanie
"czy wspolbieznosc w ogole pomoze", ZANIM ktokolwiek przepisze produkcyjny
modul - i ma pokazac przypadek, w ktorym wspolbieznosc SZKODZI.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from joboffers.bench.harness import Measurement


def run_sequential(work: Callable[[int], int], items: Sequence[int]) -> list[int]:
    """Punkt odniesienia. Bez niego kazda inna liczba jest bez znaczenia."""
    raise NotImplementedError("T11: wariant sekwencyjny")


def run_threads(work: Callable[[int], int], items: Sequence[int], workers: int) -> list[int]:
    """`ThreadPoolExecutor`."""
    raise NotImplementedError("T11: wariant watkowy")


def run_processes(work: Callable[[int], int], items: Sequence[int], workers: int) -> list[int]:
    """`ProcessPoolExecutor`.

    Zmierz OSOBNO koszt startu puli i koszt serializacji argumentow - dla
    malego `items` to one, a nie liczenie, zdominuja wynik.
    """
    raise NotImplementedError("T11: wariant procesowy")


async def run_asyncio(work: Callable[[int], int], items: Sequence[int], limit: int) -> list[int]:
    """`asyncio` z semaforem ograniczajacym rownoleglosc.

    Sensowny wylacznie dla obciazenia I/O-bound; dla CPU-bound ma pokazac,
    ze petla zdarzeń stoi (pyt-reg-003).
    """
    raise NotImplementedError("T11: wariant asynchroniczny")


def compare(
    work: Callable[[int], int],
    items: Sequence[int],
    worker_counts: Sequence[int] = (1, 2, 4, 8, 16),
) -> list[Measurement]:
    """Uruchamia wszystkie warianty dla kolejnych liczb wykonawcow.

    Zwraca liste odczytow gotowa do wpisania do docs/pomiary/.
    """
    raise NotImplementedError("T11: zestaw porownanie")


def decide(measurements: Sequence[Measurement], overhead_threshold: float = 0.10) -> str:
    """Zamienia odczyty na REKOMENDACJE i jej uzasadnienie liczba.

    Ma zwrocic jedno z rozstrzygniec:
      - "sekwencyjnie": zaden wariant nie poprawia czasu o wiecej niz prog,
        wiec wspolbieznosc dokłada zlozonosc bez zysku;
      - "watki": czas scienny maleje przy stalym czasie procesora;
      - "procesy": czas scienny maleje dopiero na procesach, a zysk przewyzsza
        koszt startu puli i serializacji;
      - "asyncio": jak watki, ale przy liczbie rownoczesnych operacji, przy
        ktorej koszt stosu na watek zaczyna sie liczyc.
    """
    raise NotImplementedError("T11: rozstrzygnij decyzje liczba")
