"""Wspolne fixture.

Zagadnienie: pyt-jun-003 - zakres fixture decyduje, ile razy zasob powstaje.
Domyslnie `function`; `session` tylko dla zasobow NIEMUTOWALNYCH.
"""

from __future__ import annotations

from datetime import date

import pytest

from joboffers.domain.models import Offer, RawOffer, Seniority


@pytest.fixture
def raw_offer() -> RawOffer:
    return RawOffer(
        source="justjoin",
        external_id="abc-123",
        payload={
            "title": "  Senior   Python Developer ",
            "company": "ACME",
            "seniority": "senior",
            "tech_stack": ["Python", "FastAPI", "python"],
            "url": "https://example.test/1",
        },
        fetched_at=date(2026, 8, 14),
    )


@pytest.fixture
def offer() -> Offer:
    return Offer(
        source="justjoin",
        external_id="abc-123",
        title="senior python developer",
        company="acme",
        seniority=Seniority.SENIOR,
        tech_stack=frozenset({"python", "fastapi"}),
        url="https://example.test/1",
    )
