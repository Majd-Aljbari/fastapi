"""DTO-Klasse für die Adresse, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

from hochschule.service.exceptions import AdresseRequiredError
lazy from hochschule.entity import Adresse

__all__ = ["AdresseDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type(name="Adresse")
class AdresseDTO:
    """DTO-Klasse für die Adresse, insbesondere ohne Decorators für SQLAlchemy."""

    strasse: str
    hausnummer: str
    plz: str
    ort: str

    @classmethod
    def from_adresse(cls, adresse: Adresse | None) -> AdresseDTO:
        """Initialisierung von AdresseDTO durch ein Entity-Objekt von Adresse.

        :param adresse: Adresse-Objekt mit Decorators für SQLAlchemy
        :return: AdresseDTO-Objekt mit Daten aus dem Adresse-Objekt
        :rtype: AdresseDTO
        :raises AdresseRequiredError: falls adresse None ist
        """
        if adresse is None:
            raise AdresseRequiredError

        return cls(
            strasse=adresse.strasse,
            hausnummer=adresse.hausnummer,
            plz=adresse.plz,
            ort=adresse.ort,
        )
