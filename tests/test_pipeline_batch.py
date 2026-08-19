"""T14 / T15 - idempotencja, wznawialnosc, rekonsyliacja (pyt-reg-007)."""

from __future__ import annotations

from datetime import date

import pytest

from joboffers.domain.models import RawOffer, ReconciliationReport
from joboffers.pipeline.batch import chunked, run_batch


def _raws(n: int) -> list[RawOffer]:
    return [
        RawOffer("fake", str(i), {"title": f"t{i}", "company": "acme"}, date(2026, 8, 14))
        for i in range(n)
    ]


def test_chunked_jest_generatorem_a_nie_lista() -> None:
    import types

    assert isinstance(chunked(iter(_raws(5)), 2), types.GeneratorType)


@pytest.mark.parametrize(("total", "size", "porcje"), [(10, 3, 4), (10, 10, 1), (0, 5, 0)])
def test_chunked_dzieli_zgodnie_z_rozmiarem(total: int, size: int, porcje: int) -> None:
    assert len(list(chunked(_raws(total), size))) == porcje


@pytest.mark.db
def test_ponowne_uruchomienie_nie_dubluje_danych() -> None:
    raws = _raws(1000)
    run_batch(raws, run_name="test-idem", batch_size=100, resume=False)
    pierwszy = sum(r.inserted for r in run_batch(raws, "test-idem", 100, resume=False))
    assert pierwszy == 0, "drugi przebieg wstawil rekordy = brak klucza idempotencji"


@pytest.mark.db
def test_wznowienie_startuje_od_kolejnej_porcji() -> None:
    wyniki = run_batch(_raws(1000), run_name="test-resume", batch_size=100, resume=True)
    assert wyniki[0].batch_no > 1, "przebieg wystartowal od zera mimo punktu kontrolnego"


def test_rekonsyliacja_zgodnych_licznikow_nie_wystarcza() -> None:
    """Rowne liczniki przy roznych sumach kontrolnych = dane uszkodzone."""
    raport = ReconciliationReport(
        window_start=date(2026, 8, 1),
        window_end=date(2026, 8, 14),
        source_count=4_218_730,
        target_count=4_218_730,
        source_checksum="aaa",
        target_checksum="bbb",
    )
    assert raport.is_consistent is False
