"""Pydantic-Modelle für das Lesen und Suchen von Hochschuldaten (GET Requests & Responses)."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from hochschule.repository import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    HochschuleSuchparameter,
    Pageable,
)
from hochschule.service import HochschuleDTO

__all__ = [
    "HochschuleFindModel",
    "HochschulePageModel",
    "HochschuleResponseModel",
]


class HochschuleFindModel(BaseModel):
    """Suchparameter und Pagination für die Hochschulsuche."""

    name: str | None = None
    page: Annotated[int, Field(ge=DEFAULT_PAGE_NUMBER)] = DEFAULT_PAGE_NUMBER
    size: Annotated[int, Field(ge=0, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE

    model_config = ConfigDict(extra="forbid", frozen=True)

    def to_pageable(self) -> Pageable:
        """Erzeugt die Pagination-Daten aus den validierten Parametern."""
        return Pageable(number=self.page, size=self.size)

    def to_suchparameter(self) -> HochschuleSuchparameter:
        """Erzeugt Suchparameter für den Service."""
        return HochschuleSuchparameter(name=self.name)


class AdresseResponseModel(BaseModel):
    """Adresse als Teil der Response."""

    strasse: str
    hausnummer: str
    plz: str
    ort: str

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")


class StudentResponseModel(BaseModel):
    """Student als Teil der Response."""

    id: int
    matrikelnummer: str
    vorname: str
    nachname: str
    email: str

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")


class HochschuleResponseModel(BaseModel):
    """Pydantic-Modell für eine gefundene Hochschule (Response JSON)."""

    id: int
    name: str
    homepage: str | None
    adresse: AdresseResponseModel | None
    studenten: list[StudentResponseModel]

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")

    @classmethod
    def from_dto(cls, hochschule: HochschuleDTO) -> "HochschuleResponseModel":
        """Konvertiert ein HochschuleDTO in ein Pydantic-Modell für den Response."""
        return cls.model_validate(hochschule)


class PageMetaModel(BaseModel):
    """Metadaten für Pagination."""

    size: int
    number: int
    total_elements: int
    total_pages: int


class HochschulePageModel(BaseModel):
    """Response-Modell bei Suche mit Pagination."""

    content: tuple[HochschuleResponseModel, ...]
    page: PageMetaModel
