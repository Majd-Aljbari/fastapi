"""GraphQL-Typen und Inputs mit Strawberry."""

from datetime import datetime
import strawberry


@strawberry.type
class AdresseType:
    id: int
    strasse: str
    hausnummer: str
    plz: str
    ort: str


@strawberry.type
class StudentType:
    id: int
    matrikelnummer: str
    vorname: str
    nachname: str
    email: str


@strawberry.type
class HochschuleType:
    id: int
    version: int
    name: str
    homepage: str | None
    erzeugt: datetime
    aktualisiert: datetime
    adresse: AdresseType | None
    studenten: list[StudentType]


@strawberry.input
class AdresseInput:
    strasse: str
    hausnummer: str
    plz: str
    ort: str


@strawberry.input
class HochschuleInput:
    name: str
    homepage: str | None = None
    adresse: AdresseInput | None = None


@strawberry.input
class Suchparameter:
    name: str | None = None


@strawberry.type
class CreatePayload:
    id: int


@strawberry.type
class LoginResult:
    token: str
    expiresIn: str
    roles: list[str]
