"""Konfiguracja logowania - JEDEN punkt w calym projekcie.

Zagadnienie: pyt-jun-006.

Kontrakt, ktory ma spelniac implementacja (zadanie T01):
1. `configure_logging()` wolane WYLACZNIE z punktu wejscia (cli.py, api/app.py,
   conftest.py). Zaden modul biblioteczny nie konfiguruje logowania sam.
2. Moduly pobieraja logger przez `logging.getLogger(__name__)` - hierarchia po
   nazwie modulu jest tym, co pozwala pozniej wlaczyc DEBUG punktowo.
3. Wywolanie dwa razy nie duplikuje handlerow.
4. Argumenty ida jako parametry (`logger.info("zapisano %s", key)`), nie f-string.
5. Pola wrazliwe sa maskowane zanim trafia do wpisu.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Literal

REDACTED = "***"
SENSITIVE_KEYS = frozenset({"password", "token", "authorization", "api_key", "secret"})


def configure_logging(
    level: str = "INFO",
    fmt: Literal["text", "json"] = "text",
) -> None:
    """Konfiguruje logger glowny: poziom, handler, formatter.

    Args:
        level: nazwa poziomu ("DEBUG", "INFO", ...).
        fmt: "text" do konsoli lokalnie, "json" gdy wpisy ida do systemu zbierania.

    Wywolanie idempotentne - drugie wywolanie nie dokłada handlera.
    """
    raise NotImplementedError("T01: skonfiguruj logowanie")


def redact(payload: Mapping[str, object]) -> dict[str, object]:
    """Zwraca kopie slownika z zamaskowanymi wartosciami kluczy wrazliwych.

    Maskowanie ma dzialac takze zagniezdzone. Klucze porownuje sie bez wzgledu
    na wielkosc liter.
    """
    raise NotImplementedError("T19: zamaskuj dane wrazliwe")


class RequestIdFilter(logging.Filter):
    """Dokłada do kazdego wpisu identyfikator zadania/przebiegu.

    Bez tego pola nie da sie zebrac wszystkich wpisow jednego zadania w
    systemie logow - a to jest cala wartosc logowania po awarii.
    """

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        raise NotImplementedError("T01: dopisz request_id/run_id do rekordu")
