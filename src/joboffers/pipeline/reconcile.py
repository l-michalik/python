"""Rekonsyliacja zrodla z celem.

Zagadnienie: pyt-reg-007.

Regula, ktora latwo zlamac: obie strony musza byc policzone NIEZALEZNYMI
sciezkami. Zestawienie liczone tym samym kodem, ktory zapisywal, potwierdza
wlasne bledy.
"""

from __future__ import annotations

import logging
from datetime import date

from joboffers.domain.models import ReconciliationReport

logger = logging.getLogger(__name__)


def reconcile(run_name: str, window_start: date, window_end: date) -> ReconciliationReport:
    """Porownuje liczbe i sume kontrolna rekordow po obu stronach okna.

    Rzuca `ReconciliationMismatch` gdy raport jest niezgodny - albo zwraca
    raport i zostawia decyzje wywolujacemu; wybierz jedno i uzasadnij w T15.
    """
    raise NotImplementedError("T15: policz obie strony niezaleznie")
