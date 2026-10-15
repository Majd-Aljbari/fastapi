"""Modul für den DB-Zugriff."""

from hochschule.repository.pageable import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    Pageable,
)
# TODO: patient_repository durch hochschule_repository ersetzen
# from hochschule.repository.patient_repository import PatientRepository
# from hochschule.repository.patient_suchparameter import PatientSuchparameter
from hochschule.repository.session_factory import Session, engine
from hochschule.repository.slice import Slice

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "DEFAULT_PAGE_NUMBER",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "Pageable",
    "Session",
    "Slice",
    "engine",
    # "PatientRepository",
    # "PatientSuchparameter",
]
