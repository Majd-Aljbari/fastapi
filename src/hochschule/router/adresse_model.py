"""Pydantic-Model für die Adresse."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from hochschule.entity import Adresse

__all__ = ["AdresseModel"]


class AdresseModel(BaseModel):
    """Pydantic-Model für die Adresse."""

    strasse: Annotated[str, StringConstraints(max_length=100)]
    """Straßenname"""
    hausnummer: Annotated[str, StringConstraints(max_length=10)]
    """Hausnummer"""
    plz: Annotated[str, StringConstraints(pattern=r"^\d{5}$")]
    """Postleitzahl (5-stellig)"""
    ort: Annotated[str, StringConstraints(max_length=64)]
    """Ort"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "strasse": "Hochschulstraße",
                "hausnummer": "1",
                "plz": "76133",
                "ort": "Karlsruhe",
            },
        },
        strict=True,
        extra="forbid",
        frozen=True,
    )

    def to_adresse(self) -> Adresse:
        """Konvertierung in ein Adresse-Objekt für SQLAlchemy."""
        return Adresse(
            id=None,
            strasse=self.strasse,
            hausnummer=self.hausnummer,
            plz=self.plz,
            ort=self.ort,
            hochschule_id=None,
            hochschule=None,
        )
