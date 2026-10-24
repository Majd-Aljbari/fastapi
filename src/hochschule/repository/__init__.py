"""Modul für den DB-Zugriff."""

from hochschule.repository.hochschule_repository import HochschuleRepository
from hochschule.repository.hochschule_suchparameter import HochschuleSuchparameter
from hochschule.repository.pageable import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    Pageable,
)
from hochschule.repository.session_factory import Session, engine
from hochschule.repository.slice import Slice

__all__ = [
    "DEFAULT_PAGE_NUMBER",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "HochschuleRepository",
    "HochschuleSuchparameter",
    "Pageable",
    "Session",
    "Slice",
    "engine",
]
