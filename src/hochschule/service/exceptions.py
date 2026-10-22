"""Exceptions in der Geschäftslogik."""

lazy from hochschule.repository.hochschule_suchparameter import HochschuleSuchparameter

__all__ = [
    "AdresseRequiredError",
    "ForbiddenError",
    "NameExistsError",
    "NotFoundError",
    "VersionOutdatedError",
]


class NameExistsError(Exception):
    """Exception, falls der Name der Hochschule bereits existiert."""

    def __init__(self, name: str) -> None:
        """Initialisierung mit dem Hochschulnamen.

        :param name: Bereits existierender Hochschulname
        """
        super().__init__(f"Existierender Hochschulname: {name}")
        self.name = name


class ForbiddenError(Exception):
    """Exception, falls der Zugriff nicht erlaubt ist."""


class NotFoundError(Exception):
    """Exception, falls keine Hochschule gefunden wurde."""

    def __init__(
        self,
        hochschule_id: int | None = None,
        suchparameter: HochschuleSuchparameter | None = None,
    ) -> None:
        """Initialisierung von NotFoundError mit ID und Suchparameter.

        :param hochschule_id: Hochschule-ID, zu der nichts gefunden wurde
        :param suchparameter: Suchparameter, zu denen nichts gefunden wurde
        """
        super().__init__("Not Found")
        self.hochschule_id = hochschule_id
        self.suchparameter = suchparameter


class VersionOutdatedError(Exception):
    """Exception, falls die Versionsnummer beim Aktualisieren veraltet ist."""

    def __init__(self, version: int) -> None:
        """Initialisierung von VersionOutdatedError mit veralteter Versionsnummer.

        :param version: Veraltete Versionsnummer
        """
        super().__init__(f"Veraltete Version: {version}")
        self.version = version


class AdresseRequiredError(RuntimeError):
    """Exception, falls eine Adresse im aktuellen Zustand None ist."""

    def __init__(self) -> None:
        """Initialisierung von AdresseRequiredError."""
        super().__init__("Ungueltiger Zustand: Adresse ist None")