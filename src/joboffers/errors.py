"""Wyjatki domenowe.

Zagadnienia: pyt-nic-004 (hierarchia wyjatkow), pyt-jun-006 (traceback).

Zasada: kazda warstwa rzuca wyjatek z tej hierarchii, a nie surowy `Exception`
ani `ValueError` bez kontekstu. Dzieki wspolnemu przodkowi wywolujacy moze
zlapac cala rodzine (`except JobOffersError`) albo jeden przypadek.
"""

from __future__ import annotations


class JobOffersError(Exception):
    """Wspolny przodek wszystkich bledow tego projektu."""


class SourceError(JobOffersError):
    """Blad pobrania danych ze zrodla zewnetrznego."""


class SourceUnavailable(SourceError):
    """Zrodlo odpowiedzialo bledem lub nie odpowiedzialo w limicie czasu."""


class MalformedOffer(JobOffersError):
    """Rekord ze zrodla nie da sie zmapowac na model domenowy."""


class StorageError(JobOffersError):
    """Blad warstwy trwalego zapisu."""


class ReconciliationMismatch(JobOffersError):
    """Rekonsyliacja wykryla rozbieznosc miedzy zrodlem a celem."""
