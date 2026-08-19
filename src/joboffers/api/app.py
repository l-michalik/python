"""Aplikacja FastAPI.

Zagadnienia: pyt-jun-004 (REST i walidacja), pyt-reg-003 (model wspolbieznosci
uslugi), pyt-reg-004 (N+1 w widoku listy), pyt-jun-006 (logowanie).

Uwaga do T05/T10: `def` i `async def` w trasie to DWA rozne modele wykonania.
Trasa `async def` wolajaca synchroniczny sterownik bazy blokuje cala petle.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from joboffers.api.schemas import OfferIn, OfferOut, OfferPage

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Fabryka aplikacji - konfiguracja logowania i zaleznosci w jednym miejscu."""
    app = FastAPI(title="joboffers", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/offers", status_code=201)
    def create_offer(payload: OfferIn) -> OfferOut:
        """Tworzy oferte. Walidacja ksztaltu dzieje sie PRZED wejsciem tutaj."""
        raise NotImplementedError("T05: utworz oferte")

    @app.get("/offers")
    def list_offers(limit: int = 100, cursor: int | None = None) -> OfferPage:
        """Lista ofert z tech-stackiem.

        T13: to jest endpoint, na ktorym mierzysz liczbe zapytan na zadanie.
        """
        raise NotImplementedError("T05: zwroc liste ofert")

    return app


app = create_app()
