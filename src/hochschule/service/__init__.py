"""Modul für die Geschäftslogik."""

from hochschule.service.adresse_dto import AdresseDTO
from hochschule.service.exceptions import (
    AdresseRequiredError,
    ForbiddenError,
    NameExistsError,
    NotFoundError,
    VersionOutdatedError,
)
from hochschule.service.hochschule_dto import HochschuleDTO
from hochschule.service.hochschule_service import HochschuleService
from hochschule.service.hochschule_write_service import HochschuleWriteService
from hochschule.service.mailer import send_mail
from hochschule.service.student_dto import StudentDTO

__all__ = [
    "AdresseDTO",
    "AdresseRequiredError",
    "ForbiddenError",
    "HochschuleDTO",
    "HochschuleService",
    "HochschuleWriteService",
    "NameExistsError",
    "NotFoundError",
    "StudentDTO",
    "VersionOutdatedError",
    "send_mail",
]
