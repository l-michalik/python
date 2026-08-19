"""Idempotentny, wznawialny potok wsadowy.

Zagadnienie: pyt-reg-007.

Trzy niezalezne wlasnosci, ktore trzeba umiec pokazac osobno:
1. IDEMPOTENCJA - ponowne przetworzenie tej samej porcji nie tworzy duplikatu.
2. WZNAWIALNOSC  - po awarii przebieg startuje od porcji N+1, nie od zera.
3. ATOMOWOSC     - dane porcji i punkt kontrolny ida JEDNA transakcja.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable, Iterator, Sequence

from joboffers.domain.models import BatchResult, RawOffer

logger = logging.getLogger(__name__)


def chunked(items: Iterable[RawOffer], size: int) -> Iterator[Sequence[RawOffer]]:
    """Dzieli strumien na porcje o zadanym rozmiarze.

    Ma byc generatorem - materializacja calosci do listy zabija sens wsadu
    (pyt-reg-002: szczyt zuzycia pamieci).
    """
    raise NotImplementedError("T14: podziel na porcje")


def run_batch(
    raws: Iterable[RawOffer],
    run_name: str,
    batch_size: int = 10_000,
    resume: bool = True,
) -> list[BatchResult]:
    """Uruchamia przebieg wsadowy z punktem kontrolnym.

    Args:
        raws: strumien rekordow zrodlowych.
        run_name: nazwa przebiegu - klucz punktu kontrolnego.
        batch_size: rozmiar porcji. Za duza porcja trzyma blokady zbyt dlugo.
        resume: True -> start od `checkpoint + 1`.

    Rekord trwale wadliwy trafia do kolejki odrzuconych i NIE zatrzymuje
    przebiegu; ponawianie ma ograniczona liczbe prob i rosnacy odstep.
    """
    raise NotImplementedError("T14: uruchom potok wsadowy")
