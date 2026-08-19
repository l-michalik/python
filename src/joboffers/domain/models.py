"""Model domenowy oferty.

Zagadnienia: pyt-nic-003 (wybor struktury danych i jej koszt),
pyt-jun-002 (adnotacje typow), pyt-reg-006 (typy jako kontrakt).

Uwaga do T03: `Offer` jest `frozen`, wiec ma stabilny skrot i moze byc
elementem `set` - to jest wprost powod, dla ktorego deduplikacja miliona
rekordow kosztuje tu stale, a nie liniowo na element.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum


class Seniority(StrEnum):
    """Poziom stanowiska wg ogloszenia."""

    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class RawOffer:
    """Rekord dokladnie taki, jaki przyszedl ze zrodla - przed normalizacja.

    Trzymamy go osobno, bo rekonsyliacja (T15) musi liczyc po stronie zrodla
    niezaleznie od sciezki, ktora dane weszly do celu.
    """

    source: str
    external_id: str
    payload: dict[str, object]
    fetched_at: date


@dataclass(frozen=True, slots=True)
class Offer:
    """Znormalizowana oferta.

    `dedup_key` jest kluczem idempotencji (T14): pochodzi z DANYCH ZRODLOWYCH,
    nigdy ze znacznika czasu przetwarzania.
    """

    source: str
    external_id: str
    title: str
    company: str
    seniority: Seniority
    tech_stack: frozenset[str] = field(default_factory=frozenset)
    url: str = ""

    @property
    def dedup_key(self) -> str:
        """Naturalny klucz zdarzenia: zrodlo + identyfikator w zrodle."""
        return f"{self.source}:{self.external_id}"


@dataclass(frozen=True, slots=True)
class BatchResult:
    """Wynik jednej porcji potoku wsadowego (T14)."""

    batch_no: int
    read: int
    inserted: int
    updated: int
    rejected: int


@dataclass(frozen=True, slots=True)
class ReconciliationReport:
    """Wynik rekonsyliacji zrodla z celem (T15).

    Sama rownosc licznikow NIE dowodzi poprawnosci - stad `source_checksum`
    i `target_checksum` liczone po polach istotnych.
    """

    window_start: date
    window_end: date
    source_count: int
    target_count: int
    source_checksum: str
    target_checksum: str

    @property
    def is_consistent(self) -> bool:
        """True tylko gdy zgadzaja sie liczniki I sumy kontrolne."""
        raise NotImplementedError("T15: rozstrzygnij zgodnosc")
