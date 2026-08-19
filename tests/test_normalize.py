"""T03 / T15 - normalizacja, deduplikacja, suma kontrolna."""

from __future__ import annotations

import pytest

from joboffers.domain.models import Offer, RawOffer, Seniority
from joboffers.errors import MalformedOffer
from joboffers.normalize.text import deduplicate, fingerprint, normalize


def test_normalize_mapuje_rekord_na_model(raw_offer: RawOffer) -> None:
    result = normalize(raw_offer)
    assert result.title == "senior python developer"
    assert result.seniority is Seniority.SENIOR
    assert result.tech_stack == frozenset({"python", "fastapi"})


def test_normalize_rzuca_na_braku_pola_wymaganego(raw_offer: RawOffer) -> None:
    uszkodzony = RawOffer(
        source=raw_offer.source,
        external_id=raw_offer.external_id,
        payload={"company": "ACME"},
        fetched_at=raw_offer.fetched_at,
    )
    with pytest.raises(MalformedOffer):
        normalize(uszkodzony)


def test_deduplicate_zachowuje_kolejnosc_pierwszego_wystapienia(offer: Offer) -> None:
    inny = Offer(
        source="justjoin",
        external_id="zzz-999",
        title="mid python developer",
        company="acme",
        seniority=Seniority.MID,
    )
    assert deduplicate([offer, inny, offer]) == [offer, inny]


def test_fingerprint_nie_zalezy_od_kolejnosci_tech_stacku() -> None:
    a = Offer("s", "1", "t", "c", Seniority.MID, frozenset({"python", "sql"}))
    b = Offer("s", "1", "t", "c", Seniority.MID, frozenset({"sql", "python"}))
    assert fingerprint(a) == fingerprint(b)


def test_fingerprint_zmienia_sie_gdy_zmieni_sie_pole_istotne(offer: Offer) -> None:
    zmieniona = Offer(offer.source, offer.external_id, "inny tytul", offer.company, offer.seniority)
    assert fingerprint(offer) != fingerprint(zmieniona)
