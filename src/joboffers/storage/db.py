"""Silnik i sesja SQLAlchemy.

Zagadnienie: pyt-jun-005 (granica transakcji, cykl zycia sesji).

Regula: JEDNA sesja na zadanie HTTP / na porcje wsadu. Nie jedna na proces.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine  # noqa: F401  (create_engine uzyjesz w T04)
from sqlalchemy.orm import Session, sessionmaker


def make_engine(database_url: str, echo_sql: bool = False) -> Engine:
    """Tworzy silnik. `echo_sql=True` wlacza logowanie zapytan - potrzebne w T13."""
    raise NotImplementedError("T04: skonfiguruj silnik i pule polaczen")


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Fabryka sesji zwiazana z silnikiem."""
    raise NotImplementedError("T04: skonfiguruj fabryke sesji")


@contextmanager
def session_scope(factory: sessionmaker[Session]) -> Iterator[Session]:
    """Sesja z jawna granica transakcji: commit na wyjsciu, rollback na wyjatku."""
    raise NotImplementedError("T04: domknij granice transakcji")
