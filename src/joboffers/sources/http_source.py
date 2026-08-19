"""Pobieranie ofert po HTTP - wariant sekwencyjny, watkowy i asynchroniczny.

Zagadnienia: pyt-jun-007 (wspolbieznosc z gotowych klockow),
pyt-reg-003 (asyncio i blokowanie petli), pyt-reg-001 (co sie zrownolegla).

WAZNE dla T09/T11: te trzy funkcje maja robic DOKLADNIE to samo i zwracac
identyczny wynik. Roznic je ma wylacznie sposob wykonania - inaczej pomiar
porownuje dwie rozne prace, a nie dwa modele wspolbieznosci.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence

from joboffers.domain.models import RawOffer

logger = logging.getLogger(__name__)


class HttpOfferSource:
    """Zrodlo czytajace oferty z endpointow HTTP."""

    name = "http"

    def __init__(self, timeout_s: float = 5.0, max_workers: int = 8) -> None:
        self.timeout_s = timeout_s
        self.max_workers = max_workers

    def fetch_one(self, url: str) -> RawOffer:
        """Pobiera jeden adres. Rzuca `SourceUnavailable` po wyczerpaniu prob.

        TODO(T09): limit czasu, ograniczona liczba ponowien z rosnacym
        odstepem, log na poziomie WARNING przy ponowieniu.
        """
        raise NotImplementedError("T09: pobierz jeden adres")

    def fetch(self, urls: Sequence[str]) -> list[RawOffer]:
        """Wariant SEKWENCYJNY - punkt odniesienia dla pomiaru w T11."""
        raise NotImplementedError("T09: wariant sekwencyjny")

    def fetch_threaded(self, urls: Sequence[str]) -> list[RawOffer]:
        """Wariant WATKOWY (`ThreadPoolExecutor`).

        Gorna granice `max_workers` wyznacza limit po drugiej stronie
        (rownoczesne polaczenia zrodla), a nie liczba rdzeni - uzasadnij
        wybrana liczbe w docs/pomiary/.
        """
        raise NotImplementedError("T09: wariant watkowy")

    async def fetch_async(self, urls: Sequence[str]) -> list[RawOffer]:
        """Wariant ASYNCHRONICZNY (`httpx.AsyncClient` + `asyncio.gather`).

        Rownoleglosc MUSI byc ograniczona semaforem - `gather` bez limitu
        wypuszcza wszystkie zadania naraz.
        """
        raise NotImplementedError("T10: wariant asynchroniczny")
