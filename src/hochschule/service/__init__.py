"""Modul für den Geschäftslogik."""

from hochschule.service.adresse_dto import AdresseDTO
from hochschule.service.exceptions import (
    EmailExistsError,
    ForbiddenError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)
from hochschule.service.mailer import send_mail
# TODO: patient_dto/service durch hochschule_dto/service ersetzen
# from hochschule.service.patient_dto import PatientDTO
# from hochschule.service.patient_service import PatientService
# from hochschule.service.patient_write_service import PatientWriteService

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "AdresseDTO",
    "EmailExistsError",
    "ForbiddenError",
    "NotFoundError",
    "UsernameExistsError",
    "VersionOutdatedError",
    "send_mail",
    # "PatientDTO",
    # "PatientService",
    # "PatientWriteService",
]
