"""Atrapa zrodla o sterowalnym opoznieniu i awaryjnosci.

Uzywana przez testy (bez sieci) oraz przez harness pomiarowy w T11, gdzie
potrzebne jest obciazenie o ZNANEJ charakterystyce: ile czasu to czekanie,
a ile liczenie.
"""

from __future__ import annotations

from collections.abc import Sequence

from joboffers.domain.models import RawOffer


class FakeOfferSource:
    """Zrodlo bez sieci: `latency_s` symuluje czekanie, `failure_rate` awarie."""

    name = "fake"

    def __init__(self, latency_s: float = 0.2, failure_rate: float = 0.0) -> None:
        self.latency_s = latency_s
        self.failure_rate = failure_rate
        self.calls = 0

    def fetch(self, urls: Sequence[str]) -> list[RawOffer]:
        """Zwraca deterministyczne rekordy po `latency_s` na kazdy adres."""
        raise NotImplementedError("T06: zaimplementuj atrape")
