from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hochschule.entity.base import Base

if TYPE_CHECKING:
    from hochschule.entity.hochschule import Hochschule


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    matrikelnummer: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    vorname: Mapped[str] = mapped_column(String(50), nullable=False)
    nachname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Foreign Key für die 1:N-Beziehung
    hochschule_id: Mapped[int] = mapped_column(
        ForeignKey("hochschule.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Rückbeziehung zur Hochschule
    hochschule: Mapped["Hochschule"] = relationship(
        "Hochschule",
        back_populates="studenten",
    )