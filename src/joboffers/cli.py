"""Punkt wejscia z linii polecen.

Zagadnienia: pyt-jun-001, pyt-jun-006 (konfiguracja logowania w punkcie wejscia).
"""

from __future__ import annotations

import argparse

from joboffers.config import get_settings
from joboffers.logging_setup import configure_logging


def main() -> None:
    """Rozdziela polecenia: fetch / batch / reconcile / bench."""
    parser = argparse.ArgumentParser(prog="joboffers")
    parser.add_argument(
        "command",
        choices=["fetch", "batch", "reconcile", "bench"],
        help="co uruchomic",
    )
    args = parser.parse_args()

    settings = get_settings()
    configure_logging(settings.log_level, settings.log_format)  # type: ignore[arg-type]

    raise NotImplementedError(f"T00: podepnij polecenie {args.command!r}")


if __name__ == "__main__":
    main()
