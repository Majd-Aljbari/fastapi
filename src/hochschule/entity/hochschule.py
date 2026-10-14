from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hochschule.entity.base import Base

if TYPE_CHECKING:
    from hochschule.entity.adresse import Adresse
    from hochschule.entity.student import Student


class Hochschule(Base):
    __tablename__ = "hochschule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    kuerzel: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    # 1:1-Beziehung zu Adresse (uselist=False kennzeichnet die 1:1-Beziehung)
    adresse: Mapped["Adresse"] = relationship(
        "Adresse",
        back_populates="hochschule",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # 1:N-Beziehung zu Studenten (eine Hochschule hat eine Liste von Studenten)
    studenten: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="hochschule",
        cascade="all, delete-orphan",
    )
