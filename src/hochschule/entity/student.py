"""Entity-Klasse für den Studenten."""

from typing import Optional, override

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hochschule.entity.base import Base


class Student(Base):
    """Entity-Klasse für den Studenten."""

    __tablename__ = "student"

    matrikelnummer: Mapped[str]
    """Die Matrikelnummer."""

    vorname: Mapped[str]
    """Der Vorname."""

    nachname: Mapped[str]
    """Der Nachname."""

    email: Mapped[str]
    """Die Emailadresse."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    # Foreign Key für die 1:N-Beziehung
    hochschule_id: Mapped[int | None] = mapped_column(ForeignKey("hochschule.id"))
    """ID der zugehörigen Hochschule als Fremdschlüssel in der DB-Tabelle."""

    # Rückbeziehung zur Hochschule
    hochschule: Mapped[Optional["Hochschule"]] = relationship(back_populates="studenten")
    """Das zugehörige transiente Hochschule-Objekt."""

    # __repr__ fuer Entwickler/innen, __str__ fuer User
    @override
    def __repr__(self) -> str:
        """Ausgabe eines Studenten als String ohne die Hochschuldaten."""
        return (
            f"Student(id={self.id}, matrikelnummer={self.matrikelnummer}, "
            f"vorname={self.vorname}, nachname={self.nachname}, email={self.email})"
        )
