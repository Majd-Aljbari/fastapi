"""Pydantic-Model für Studentendaten."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

from hochschule.entity import Student

__all__ = ["StudentModel"]


class StudentModel(BaseModel):
    """Pydantic-Model für das Anlegen eines Studenten."""

    matrikelnummer: Annotated[str, StringConstraints(pattern=r"^\d{6,10}$")]
    """Eindeutige Matrikelnummer"""
    vorname: Annotated[str, StringConstraints(max_length=50)]
    """Vorname"""
    nachname: Annotated[str, StringConstraints(max_length=50)]
    """Nachname"""
    email: EmailStr
    """Eindeutige E-Mail-Adresse"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "matrikelnummer": "801234",
                "vorname": "Max",
                "nachname": "Mustermann",
                "email": "max.mustermann@stud.hs.de",
            },
        },
        strict=True,
        extra="forbid",
        frozen=True,
    )

    def to_student(self) -> Student:
        """Konvertierung in ein Student-Objekt für SQLAlchemy."""
        return Student(
            id=None,
            matrikelnummer=self.matrikelnummer,
            vorname=self.vorname,
            nachname=self.nachname,
            email=self.email,
            hochschule_id=None,
            hochschule=None,
        )
