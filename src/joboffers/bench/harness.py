"""Pomiar czasu sciennego i czasu procesora.

Zagadnienia: pyt-reg-001 (co naprawde sie zrownolegla), pyt-reg-002 (profil).

Sedno: SAM czas scienny nie odroznia "rownolegle" od "na zmiane". Dopiero
stosunek czasu procesora do sciennego to rozstrzyga:

    cpu/wall ~ 1  przy N wykonawcach -> rownoleglosci NIE MA
    cpu/wall ~ N                     -> praca idzie na N rdzeniach
    cpu/wall << 1                    -> obciazenie zdominowane czekaniem
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Measurement:
    """Pojedynczy odczyt."""

    label: str
    workers: int
    wall_s: float
    cpu_s: float

    @property
    def cpu_ratio(self) -> float:
        """Czas procesora / czas scienny."""
        return self.cpu_s / self.wall_s if self.wall_s else 0.0

    def __str__(self) -> str:
        return (
            f"{self.label:<28} workers={self.workers:>3}  "
            f"wall={self.wall_s:7.3f}s  cpu={self.cpu_s:7.3f}s  "
            f"cpu/wall={self.cpu_ratio:5.2f}"
        )


def measure[T](label: str, workers: int, run: Callable[[], T]) -> tuple[Measurement, T]:
    """Mierzy jedno uruchomienie `run` czasem sciennym i czasem procesora.

    `time.process_time()` liczy czas CPU wszystkich WATKOW tego procesu, ale
    NIE liczy czasu procesow potomnych - dla puli procesow trzeba siegnac po
    `time.perf_counter()` plus `resource.getrusage(RUSAGE_CHILDREN)`.
    Ta pulapka jest czescia zadania T11.
    """
    wall0, cpu0 = time.perf_counter(), time.process_time()
    result = run()
    return (
        Measurement(label, workers, time.perf_counter() - wall0, time.process_time() - cpu0),
        result,
    )


def repeat[T](label: str, workers: int, run: Callable[[], T], times: int = 5) -> Measurement:
    """Powtarza pomiar i zwraca NAJLEPSZY odczyt.

    Pojedynczy przebieg mierzy glownie stan pamieci podrecznej (pyt-reg-002).
    """
    raise NotImplementedError("T11: powtorz pomiar i wybierz odczyt odporny na szum")
