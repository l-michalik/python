"""T11 - czy wspolbieznosc w ogole pomoze (pyt-reg-001, pyt-nic-005).

To sa testy WLASNOSCI POMIARU, nie testy wydajnosci. Sprawdzaja, czy harness
potrafi odroznic "rownolegle" od "na zmiane" - bo bez tego kazda decyzja
o watkach i procesach jest zgadywaniem.
"""

from __future__ import annotations

import pytest

from joboffers.bench.concurrency import compare, decide, run_sequential, run_threads
from joboffers.bench.harness import Measurement, measure
from joboffers.bench.workloads import cpu_bound, io_bound


def test_measurement_liczy_stosunek_cpu_do_sciennego() -> None:
    m = Measurement("x", 4, wall_s=1.0, cpu_s=3.6)
    assert m.cpu_ratio == pytest.approx(3.6)


def test_measure_zwraca_oba_czasy() -> None:
    m, wynik = measure("suma", 1, lambda: sum(range(100_000)))
    assert wynik == sum(range(100_000))
    assert m.wall_s > 0
    assert m.cpu_s > 0


def test_warianty_daja_identyczny_wynik() -> None:
    items = list(range(8))
    assert run_sequential(io_bound, items) == run_threads(io_bound, items, workers=4)


@pytest.mark.slow
def test_praca_liczaca_nie_zrownolegla_sie_na_watkach() -> None:
    """Podpis GIL-a: cpu/wall zostaje przy 1 mimo N watkow."""
    items = [200_000] * 4
    odczyty = compare(cpu_bound, items, worker_counts=(1, 4))
    watkowy = next(m for m in odczyty if m.label.startswith("threads") and m.workers == 4)
    assert watkowy.cpu_ratio < 1.5, (
        f"cpu/wall blisko 1 przy 4 watkach = rownoleglosci nie ma; odczyt: {watkowy}"
    )


@pytest.mark.slow
def test_praca_czekajaca_zrownolegla_sie_na_watkach() -> None:
    """Podpis I/O-bound: czas scienny maleje, czas procesora stoi."""
    items = [1] * 16
    odczyty = compare(io_bound, items, worker_counts=(1, 8))
    jeden = next(m for m in odczyty if m.label.startswith("threads") and m.workers == 1)
    osiem = next(m for m in odczyty if m.label.startswith("threads") and m.workers == 8)
    assert osiem.wall_s < jeden.wall_s / 3
    assert osiem.cpu_s == pytest.approx(jeden.cpu_s, rel=0.5)


@pytest.mark.slow
def test_decide_odradza_wspolbieznosc_gdy_zysk_ponizej_progu() -> None:
    """Najwazniejszy przypadek: system, ktorego NIE warto zrownoleglac."""
    odczyty = [
        Measurement("sequential", 1, wall_s=1.00, cpu_s=1.00),
        Measurement("threads", 4, wall_s=0.97, cpu_s=1.02),
        Measurement("processes", 4, wall_s=1.40, cpu_s=1.05),
    ]
    assert decide(odczyty, overhead_threshold=0.10) == "sekwencyjnie"


def test_decide_wskazuje_procesy_dopiero_gdy_pokryja_koszt_startu() -> None:
    odczyty = [
        Measurement("sequential", 1, wall_s=4.00, cpu_s=4.00),
        Measurement("threads", 4, wall_s=4.10, cpu_s=4.15),
        Measurement("processes", 4, wall_s=1.30, cpu_s=4.60),
    ]
    assert decide(odczyty) == "procesy"
