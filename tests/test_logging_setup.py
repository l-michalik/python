"""T01 / T19 - logowanie i maskowanie danych wrazliwych (pyt-jun-006)."""

from __future__ import annotations

import logging

import pytest

from joboffers.logging_setup import REDACTED, configure_logging, redact


def test_configure_logging_jest_idempotentne() -> None:
    root = logging.getLogger()
    configure_logging("INFO")
    po_pierwszym = len(root.handlers)
    configure_logging("INFO")
    assert len(root.handlers) == po_pierwszym


def test_logger_niesie_nazwe_modulu(caplog: pytest.LogCaptureFixture) -> None:
    configure_logging("INFO")
    logger = logging.getLogger("joboffers.sources.http_source")
    with caplog.at_level(logging.INFO):
        logger.info("pobrano %s ofert", 3)
    assert caplog.records[0].name == "joboffers.sources.http_source"
    # Argument jako parametr, nie sklejony f-string - inaczej nie da sie grupowac.
    assert caplog.records[0].args == (3,)


def test_wyjatek_loguje_sie_z_tracebackiem(caplog: pytest.LogCaptureFixture) -> None:
    configure_logging("INFO")
    logger = logging.getLogger("joboffers.test")
    with caplog.at_level(logging.ERROR):
        try:
            raise OSError("dysk pelny")
        except OSError:
            logger.exception("zapis nie powiodl sie")
    assert caplog.records[0].exc_info is not None


def test_redact_maskuje_takze_zagniezdzone() -> None:
    dane = {"user": "ala", "Password": "tajne", "auth": {"token": "xyz"}}
    wynik = redact(dane)
    assert wynik["user"] == "ala"
    assert wynik["Password"] == REDACTED
    assert wynik["auth"] == {"token": REDACTED}
