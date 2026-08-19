"""Konfiguracja aplikacji czytana ze srodowiska.

Zagadnienia: pyt-jun-001 (srodowisko projektu), pyt-jun-004 (walidacja w
czasie dzialania po stronie granicy).

TODO(T00): uzupelnij pola, ktorych projekt faktycznie potrzebuje, i dopisz
`.env.example`. Sekrety NIE wchodza do repozytorium.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ustawienia czytane z `.env` i zmiennych srodowiskowych."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="JOBOFFERS_")

    database_url: str = "postgresql+psycopg://joboffers:joboffers@localhost:5432/joboffers"
    log_level: str = "INFO"
    log_format: str = "text"  # "text" | "json" - patrz T01
    http_timeout_s: float = 5.0
    fetch_max_workers: int = 8
    batch_size: int = 10_000


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Zwraca jedna instancje ustawien na proces."""
    return Settings()
