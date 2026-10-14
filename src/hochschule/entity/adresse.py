from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hochschule.entity.base import Base

if TYPE_CHECKING:
    from hochschule.entity.hochschule import Hochschule


class Adresse(Base):
    __tablename__ = "adresse"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    strasse: Mapped[str] = mapped_column(String(100), nullable=False)
    hausnummer: Mapped[str] = mapped_column(String(10), nullable=False)
    plz: Mapped[str] = mapped_column(String(10), nullable=False)
    ort: Mapped[str] = mapped_column(String(100), nullable=False)

    # Foreign Key für die 1:1-Beziehung zu Hochschule (unique=True erzwingt 1:1)
    hochschule_id: Mapped[int] = mapped_column(
        ForeignKey("hochschule.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Rückbeziehung zur Hochschule
    hochschule: Mapped["Hochschule"] = relationship(
        "Hochschule",
        back_populates="adresse",
    )
