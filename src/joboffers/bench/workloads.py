"""Dwa obciazenia o znanej charakterystyce - material do porownania w T11.

Zagadnienia: pyt-nic-005, pyt-reg-001.

Kluczowa wlasnosc: oba maja miec PODOBNY czas sekwencyjny, zeby porownanie
dotyczylo modelu wykonania, a nie rozmiaru pracy.
"""

from __future__ import annotations


def io_bound(n: int) -> int:
    """Czekanie - odpowiednik zadania sieciowego.

    Realizowane przez uspienie, nie przez petle - uspienie zwalnia GIL
    dokladnie tak, jak zrobiloby to zadanie na gniezdzie.
    """
    raise NotImplementedError("T11: obciazenie I/O-bound")


def cpu_bound(n: int) -> int:
    """Liczenie w czystym Pythonie - odpowiednik normalizacji tekstu.

    NIE wolno tu uzyc NumPy ani innej biblioteki natywnej: biblioteka
    natywna zwalnia GIL, wiec pomiar pokazalby rownoleglosc, ktorej twoja
    petla nie ma (pyt-reg-001, sekcja Ograniczenia).
    """
    raise NotImplementedError("T11: obciazenie CPU-bound")


def mixed_bound(n: int) -> int:
    """Realistyczny przypadek: pobranie + normalizacja jednej oferty."""
    raise NotImplementedError("T11: obciazenie mieszane")
