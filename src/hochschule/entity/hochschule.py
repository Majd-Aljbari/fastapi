"""Entity-Klasse für Hochschuldaten."""

from typing import Self, override
lazy from dataclasses import InitVar
lazy from datetime import date, datetime

from sqlalchemy import JSON, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, reconstructor, relationship

from hochschule.entity.adresse import Adresse
from hochschule.entity.base import Base
from hochschule.entity.student import Student


class Hochschule(Base):
    """Entity-Klasse für Hochschuldaten."""

    __tablename__ = "hochschule"

    id: Mapped[int | None] = mapped_column(Identity(start=1000), primary_key=True)
    """Die generierte ID"""

    name: Mapped[str]
    """Name der Hochschule"""

    homepage: Mapped[str | None]
    """Die optionale URL der Homepage."""

    adresse: Mapped["Adresse" | None] = relationship(
        back_populates=lambda: Adresse.hochschule,
        innerjoin=True,
        cascade="save-update, delete",
    )
    """ 1:1-Beziehung zu Adresse """

    # 1:N-Beziehung zu Studenten (eine Hochschule hat eine Liste von Studenten)
    studenten: Mapped[list["Student"]] = relationship(
         back_populates=lambda: Student.hochschule,
        cascade="save-update, delete",
    )
    """ 1:N-Beziehung zu Studenten """

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
    )
    """Der Zeitstempel für das initiale INSERT in die DB-Tabelle."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
    )
    """Der Zeitstempel vom letzen UPDATE in der DB-Tabelle."""

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Die Versionsnummer für optimistische Synchronisation."""

    __mapper_args__ = {"version_id_col": version}  # ruff: ignore[mutable-class-default]

    def set(self, hochschule: Self) -> None:
        """Primitive Attributwerte überschreiben, z.B. vor einem DB-Update.

        :param hochschule: Hochschule-Objekt mit den neuen Daten
        """
        self.name = hochschule.name
        self.homepage = hochschule.homepage

    @override
    def __eq__(self, other: object) -> bool:
        """Vergleich auf Gleichheit anhand der ID, ohne Joins auszulösen."""
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Funktion anhand der ID, ohne Joins auszulösen."""
        return hash(self.id) if self.id is not None else hash(type(self))

    @override
    def __repr__(self) -> str:
        """String-Repräsentation für Entwickler/innen, ohne Joins auszulösen."""
        return (
            f"Hochschule(id={self.id}, version={self.version}, "
            f"name='{self.name}', homepage='{self.homepage}', "
            f"erzeugt={self.erzeugt}, aktualisiert={self.aktualisiert})"
        )
