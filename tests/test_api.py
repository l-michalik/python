"""T05 / T13 - warstwa HTTP i liczba zapytan (pyt-jun-004, pyt-reg-004)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from joboffers.api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}


@pytest.mark.parametrize(
    "payload",
    [
        {"source": "", "external_id": "1", "title": "t", "company": "c"},
        {"source": "s", "external_id": "1", "title": "", "company": "c"},
        {"source": "s", "external_id": "1", "title": "t", "company": "c", "url": "x" * 1001},
    ],
)
def test_niepoprawne_wejscie_odrzucane_przed_wejsciem_do_funkcji(
    client: TestClient, payload: dict[str, str]
) -> None:
    assert client.post("/offers", json=payload).status_code == 422


def test_utworzenie_zwraca_201(client: TestClient) -> None:
    r = client.post(
        "/offers",
        json={
            "source": "justjoin",
            "external_id": "1",
            "title": "Python Developer",
            "company": "ACME",
            "seniority": "mid",
            "tech_stack": ["Python"],
        },
    )
    assert r.status_code == 201


def test_odpowiedz_nie_wynosi_pol_wewnetrznych(client: TestClient) -> None:
    r = client.post(
        "/offers",
        json={"source": "s", "external_id": "1", "title": "t", "company": "c"},
    )
    assert set(r.json()) <= {"id", "title", "company", "seniority", "tech_stack", "url"}


@pytest.mark.db
def test_liczba_zapytan_widoku_listy_jest_stala_wzgledem_limitu() -> None:
    """T13: to jest DOWOD naprawy N+1 - liczba zapytan, nie czas."""
    pytest.skip("T13: podlacz licznik zapytan (event 'before_cursor_execute') i odblokuj")
