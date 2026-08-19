"""Kontrakty miedzy warstwami wyrazone strukturalnie.

Zagadnienie: pyt-reg-006 (Protocol zamiast klasy bazowej - brak zaleznosci
w druga strone, wiec `domain` nie importuje `storage` ani `sources`).
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Protocol, runtime_checkable

from joboffers.domain.models import Offer, RawOffer


@runtime_checkable
class OfferSource(Protocol):
    """Zrodlo ofert. Implementacje: HTTP, plik, atrapa w testach."""

    name: str

    def fetch(self, urls: Sequence[str]) -> list[RawOffer]:
        """Pobiera rekordy dla podanych adresow. Rzuca `SourceUnavailable`."""
        ...


@runtime_checkable
class OfferRepository(Protocol):
    """Trwaly zapis ofert."""

    def upsert_many(self, offers: Iterable[Offer]) -> tuple[int, int]:
        """Wstawia albo aktualizuje po `dedup_key`.

        Returns:
            (liczba wstawionych, liczba zaktualizowanych)
        """
        ...

    def count(self) -> int:
        """Liczba ofert w celu."""
        ...


@runtime_checkable
class Checkpoint(Protocol):
    """Trwaly znacznik postepu potoku wsadowego (T14)."""

    def read(self, run_name: str) -> int:
        """Numer ostatniej UKONCZONEJ porcji, 0 gdy przebiegu nie bylo."""
        ...

    def write(self, run_name: str, batch_no: int) -> None:
        """Zapisuje postep. MUSI isc w tej samej transakcji co dane porcji."""
        ...
