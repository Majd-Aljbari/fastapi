"""Pydantic-Model für das Anlegen von Hochschuldaten (POST Request)."""

from typing import Final, override

from loguru import logger
from pydantic import ConfigDict

from hochschule.entity import Hochschule
from hochschule.router.adresse_model import AdresseModel
from hochschule.router.hochschule_update_model import HochschuleUpdateModel
from hochschule.router.student_model import StudentModel

__all__ = ["HochschuleModel"]


class HochschuleModel(HochschuleUpdateModel):
    """Pydantic-Model für das Anlegen neuer Hochschuldaten."""

    adresse: AdresseModel
    """Die 1:1-zugehörige Adresse."""
    studenten: list[StudentModel] = []
    """Die 1:N-Liste der Studenten."""

    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)

    @override
    def to_hochschule(self) -> Hochschule:
        """Konvertierung in ein Hochschule-Objekt für SQLAlchemy (inkl. Beziehungen)."""
        logger.debug("self={}", self)
        hochschule: Final = super().to_hochschule()
        hochschule.adresse = self.adresse.to_adresse()
        hochschule.studenten = [
            student_model.to_student() for student_model in self.studenten
        ]
        logger.debug("hochschule={}", hochschule)
        return hochschule
