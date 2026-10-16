"""DTO-Klasse für Hochschuldaten, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

from hochschule.entity import Hochschule
from hochschule.service.adresse_dto import AdresseDTO
from hochschule.service.student_dto import StudentDTO

__all__ = ["HochschuleDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type(name="Hochschule")
class HochschuleDTO:
    """DTO-Klasse für ausgelesene oder gespeicherte Hochschuldaten: ohne Decorators."""

    id: int
    version: int
    name: str
    homepage: str | None
    adresse: AdresseDTO | None
    studenten: list[StudentDTO]

    @classmethod
    def from_hochschule(cls, hochschule: Hochschule) -> "HochschuleDTO":
        """Initialisierung von HochschuleDTO durch ein Entity-Objekt von Hochschule.

        :param hochschule: Hochschule-Objekt mit Decorators zu SQLAlchemy
        :return: HochschuleDTO-Objekt mit Daten aus dem Hochschule-Objekt
        :rtype: HochschuleDTO
        """
        return cls(
            id=hochschule.id if hochschule.id is not None else -1,
            version=hochschule.version,
            name=hochschule.name,
            homepage=hochschule.homepage,
            adresse=(
                AdresseDTO.from_adresse(hochschule.adresse)
                if hochschule.adresse is not None
                else None
            ),
            studenten=(
                [StudentDTO.from_student(student) for student in hochschule.studenten]
                if hochschule.studenten is not None
                else []
            ),
        )
