"""Pydantic-Model zum Aktualisieren von Hochschuldaten (PUT Request)."""

from datetime import datetime
from typing import Annotated

from loguru import logger
from pydantic import BaseModel, ConfigDict, HttpUrl, StringConstraints

from hochschule.entity import Hochschule

__all__ = ["HochschuleUpdateModel"]


class HochschuleUpdateModel(BaseModel):
    """Pydantic-Model zum Aktualisieren von Hochschuldaten."""

    name: Annotated[str, StringConstraints(min_length=2, max_length=100)]
    """Der Name der Hochschule."""
    homepage: HttpUrl | None = None
    """Die optionale URL der Homepage."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Hochschule Karlsruhe",
                "homepage": "https://www.h-ka.de",
            },
        },
        strict=True,
        extra="forbid",
        frozen=True,
    )

    def to_hochschule(self) -> Hochschule:
        """Konvertierung in ein Hochschule-Objekt für SQLAlchemy (ohne Beziehungen)."""
        logger.debug("self={}", self)
        hochschule = Hochschule(
            id=None,
            name=self.name,
            homepage=str(self.homepage) if self.homepage is not None else None,
            adresse=None,
            studenten=[],
            erzeugt=datetime.now(),
            aktualisiert=datetime.now(),
        )
        logger.debug("hochschule={}", hochschule)
        return hochschule

    # def to_hochschule(self) -> Hochschule:
    #    """Konvertierung in ein Hochschule-Objekt für SQLAlchemy (ohne Beziehungen)."""
    #     logger.debug("self={}", self)
    #     hochschule = Hochschule(
    #         #id=None,
    #         name=self.name,
    #         homepage=str(self.homepage) if self.homepage is not None else None,
    #         adresse=None,
    #         studenten=[],
    #         erzeugt=datetime.now(),
    #         aktualisiert=datetime.now(),
    #     )
    #     logger.debug("hochschule={}", hochschule)
    #     return hochschule
