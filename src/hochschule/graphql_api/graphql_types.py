"""GraphQL-Typen und Inputs mit Strawberry."""

lazy from datetime import datetime

import strawberry


@strawberry.type
class AdresseType:
    """GraphQL-Typ für eine Adresse."""

    id: int
    strasse: str
    hausnummer: str
    plz: str
    ort: str


@strawberry.type
class StudentType:
    """GraphQL-Typ für einen Studenten."""

    id: int
    matrikelnummer: str
    vorname: str
    nachname: str
    email: str


@strawberry.type
class HochschuleType:
    """GraphQL-Typ für eine Hochschule."""

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
    """GraphQL-Input für eine Adresse."""

    strasse: str
    hausnummer: str
    plz: str
    ort: str


@strawberry.input
class HochschuleInput:
    """GraphQL-Input zum Anlegen einer Hochschule."""

    name: str
    homepage: str | None = None
    adresse: AdresseInput | None = None


@strawberry.input
class Suchparameter:
    """GraphQL-Input für Suchparameter."""

    name: str | None = None


@strawberry.type
class CreatePayload:
    """GraphQL-Typ für das Ergebnis einer Mutation."""

    id: int


@strawberry.type
class LoginResult:
    """GraphQL-Typ für das Login-Ergebnis."""

    token: str
    expires_in: str
    roles: list[str]
