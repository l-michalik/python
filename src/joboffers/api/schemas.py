"""Modele wejscia i wyjscia HTTP.

Zagadnienie: pyt-jun-004 (walidacja na granicy, kontrakt w OpenAPI).

Dwie rzeczy do pilnowania w T05:
1. Model ODPOWIEDZI jest osobny od modelu ORM - inaczej pola wewnetrzne
   wyciekaja do klienta.
2. Kazde pole liczbowe i tekstowe ma GORNA granice.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from joboffers.domain.models import Seniority


class OfferIn(BaseModel):
    """Cialo zadania tworzacego oferte."""

    source: str = Field(min_length=1, max_length=50)
    external_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    company: str = Field(min_length=1, max_length=200)
    seniority: Seniority = Seniority.UNKNOWN
    tech_stack: list[str] = Field(default_factory=list, max_length=50)
    url: str = Field(default="", max_length=1000)


class OfferOut(BaseModel):
    """Reprezentacja oferty w odpowiedzi - swiadomie wezsza niz wiersz tabeli."""

    id: int
    title: str
    company: str
    seniority: Seniority
    tech_stack: list[str]
    url: str


class OfferPage(BaseModel):
    """Strona wynikow. Paginacja po kluczu, nie po `OFFSET` (patrz T13)."""

    items: list[OfferOut]
    next_cursor: int | None = None
