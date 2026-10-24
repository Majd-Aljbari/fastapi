"""Entity-Klasse für die Adresse."""

from typing import TYPE_CHECKING, override

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hochschule.entity.base import Base

if TYPE_CHECKING:
    from hochschule.entity.hochschule import Hochschule


class Adresse(Base):
    """Entity-Klasse für die Adresse."""

    __tablename__ = "adresse"

    strasse: Mapped[str]
    """Die Straße."""

    hausnummer: Mapped[str]
    """Die Hausnummer."""

    plz: Mapped[str]
    """Die Postleitzahl."""

    ort: Mapped[str]
    """Der Ort."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    # Foreign Key für die 1:1-Beziehung zu Hochschule (unique=True erzwingt 1:1)
    hochschule_id: Mapped[int | None] = mapped_column(
        ForeignKey("hochschule.id"), unique=True
    )
    """ID der zugehörigen Hochschule als Fremdschlüssel in der DB-Tabelle."""

    # Rückbeziehung zur Hochschule
    hochschule: Mapped[Hochschule | None] = relationship(back_populates="adresse")
    """Das zugehörige transiente Hochschule-Objekt."""

    # __repr__ fuer Entwickler/innen, __str__ fuer User
    @override
    def __repr__(self) -> str:
        """Ausgabe einer Adresse als String ohne die Hochschuldaten."""
        return (
            f"Adresse(id={self.id}, strasse={self.strasse}, "
            f"hausnummer={self.hausnummer}, plz={self.plz}, ort={self.ort})"
        )
