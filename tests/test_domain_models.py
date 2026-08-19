"""T03 - model domenowy i koszt struktur (pyt-nic-003, pyt-nic-004)."""

from __future__ import annotations

import pytest

from joboffers.domain.models import Offer, Seniority


def test_dedup_key_pochodzi_z_danych_zrodlowych(offer: Offer) -> None:
    assert offer.dedup_key == "justjoin:abc-123"


def test_offer_jest_hashowalna_wiec_moze_byc_w_zbiorze(offer: Offer) -> None:
    # To jest wprost powod, dla ktorego deduplikacja nie musi byc kwadratowa.
    assert len({offer, offer}) == 1


def test_seniority_nieznana_etykieta_nie_wywraca_programu() -> None:
    from joboffers.normalize.text import parse_seniority

    assert parse_seniority("architekt") is Seniority.UNKNOWN


@pytest.mark.parametrize(
    ("surowy", "oczekiwany"),
    [
        ("  Senior   Python  ", "senior python"),
        ("PYTHON", "python"),
        ("", ""),
        ("a\tb\nc", "a b c"),
    ],
)
def test_clean_text_granice_dziedziny(surowy: str, oczekiwany: str) -> None:
    from joboffers.normalize.text import clean_text

    assert clean_text(surowy) == oczekiwany
