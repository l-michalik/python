"""Mapowanie ORM.

Zagadnienia: pyt-jun-005 (model -> tabela, migracje), pyt-reg-004 (N+1).

Uwaga do T13: relacja `Offer.tags` jest CELOWO domyslnie leniwa. Widok listy
w `api/app.py` ma na starcie problem N+1 - zadanie polega na udowodnieniu go
liczba zapytan, a dopiero potem na naprawie.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Wspolna baza modeli."""


class CompanyRow(Base):
    """Pracodawca."""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)

    offers: Mapped[list[OfferRow]] = relationship(back_populates="company")


class OfferRow(Base):
    """Oferta. `dedup_key` jest kluczem idempotencji potoku (T14)."""

    __tablename__ = "offers"
    __table_args__ = (UniqueConstraint("dedup_key", name="uq_offers_dedup_key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    dedup_key: Mapped[str] = mapped_column(String(300))
    source: Mapped[str] = mapped_column(String(50))
    external_id: Mapped[str] = mapped_column(String(200))
    title: Mapped[str] = mapped_column(String(300))
    seniority: Mapped[str] = mapped_column(String(20))
    url: Mapped[str] = mapped_column(String(1000), default="")
    fingerprint: Mapped[str] = mapped_column(String(64), default="")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company: Mapped[CompanyRow] = relationship(back_populates="offers")

    tags: Mapped[list[TagRow]] = relationship(back_populates="offer")


class TagRow(Base):
    """Element tech-stacku oferty (relacja jeden-do-wielu -> zrodlo N+1)."""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id"))
    name: Mapped[str] = mapped_column(String(80))

    offer: Mapped[OfferRow] = relationship(back_populates="tags")


class CheckpointRow(Base):
    """Punkt kontrolny potoku wsadowego (T14)."""

    __tablename__ = "checkpoints"

    run_name: Mapped[str] = mapped_column(String(100), primary_key=True)
    batch_no: Mapped[int] = mapped_column(default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
