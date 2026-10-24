"""DTO-Klasse für Studenten, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

lazy from hochschule.entity import Student

__all__ = ["StudentDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type(name="Student")
class StudentDTO:
    """DTO-Klasse für ausgelesene oder gespeicherte Studentendaten: ohne Decorators."""

    id: int
    matrikelnummer: str
    vorname: str
    nachname: str
    email: str

    @classmethod
    def from_student(cls, student: Student) -> StudentDTO:
        """Initialisierung von StudentDTO durch ein Entity-Objekt von Student.

        :param student: Student-Objekt mit Decorators für SQLAlchemy
        :return: StudentDTO-Objekt mit Daten aus dem Student-Objekt
        :rtype: StudentDTO
        """
        return cls(
            id=student.id if student.id is not None else -1,
            matrikelnummer=student.matrikelnummer,
            vorname=student.vorname,
            nachname=student.nachname,
            email=student.email,
        )
