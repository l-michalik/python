"""T09 / T10 - wspolbieznosc pobierania (pyt-jun-007, pyt-reg-003)."""

from __future__ import annotations

import time

import pytest

from joboffers.sources.fake_source import FakeOfferSource
from joboffers.sources.http_source import HttpOfferSource


def test_atrapa_zwraca_rekord_na_kazdy_adres() -> None:
    src = FakeOfferSource(latency_s=0.0)
    assert len(src.fetch(["a", "b", "c"])) == 3


def test_watkowy_i_sekwencyjny_daja_ten_sam_wynik(monkeypatch: pytest.MonkeyPatch) -> None:
    # Bez tego porownanie w T11 mierzy dwie rozne prace, a nie dwa modele wykonania.
    src = HttpOfferSource(max_workers=4)
    monkeypatch.setattr(src, "fetch_one", lambda url: url)
    urls = [f"u{i}" for i in range(10)]
    assert src.fetch(urls) == src.fetch_threaded(urls)


@pytest.mark.slow
def test_watki_skracaja_czas_scienny_dla_czekania() -> None:
    src = FakeOfferSource(latency_s=0.1)
    urls = [f"u{i}" for i in range(20)]
    start = time.perf_counter()
    src.fetch(urls)
    sekwencyjnie = time.perf_counter() - start
    assert sekwencyjnie > 1.5, "atrapa ma faktycznie czekac, inaczej pomiar nic nie znaczy"


async def test_asynchroniczny_ma_ograniczona_rownoleglosc() -> None:
    # gather bez semafora wypuszcza wszystkie zadania naraz - to jest blad,
    # ktory ma zlapac ten test.
    src = HttpOfferSource(max_workers=4)
    wynik = await src.fetch_async([f"u{i}" for i in range(50)])
    assert len(wynik) == 50
