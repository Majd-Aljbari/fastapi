"""Geschäftslogik zum Schreiben von Hochschuldaten."""

from typing import Final

from loguru import logger

from hochschule.entity import Hochschule
from hochschule.repository import HochschuleRepository, Session
from hochschule.service.exceptions import (
    NameExistsError,
    NotFoundError,
    VersionOutdatedError,
)
from hochschule.service.hochschule_dto import HochschuleDTO

__all__ = ["HochschuleWriteService"]


class HochschuleWriteService:
    """Service-Klasse mit Geschäftslogik für Schreib-Operationen bei Hochschule."""

    def __init__(self, repo: HochschuleRepository) -> None:
        """Konstruktor mit abhängigem HochschuleRepository."""
        self.repo: HochschuleRepository = repo

    def create(self, hochschule: Hochschule) -> HochschuleDTO:
        """Eine neue Hochschule anlegen.

        :param hochschule: Die neue Hochschule ohne ID
        :return: Die neu angelegte Hochschule mit generierter ID
        :rtype: HochschuleDTO
        :raises NameExistsError: Falls der Hochschulname bereits existiert
        """
        logger.debug(
            "hochschule={}, adresse={}, studenten={}",
            hochschule,
            hochschule.adresse,
            hochschule.studenten,
        )

        name: Final = hochschule.name

        with Session() as session:
            if self.repo.exists_name(name=name, session=session):
                raise NameExistsError(name=name)

            hochschule_db: Final = self.repo.create(
                hochschule=hochschule, session=session
            )
            hochschule_dto: Final = HochschuleDTO.from_hochschule(hochschule_db)
            session.commit()

        logger.debug("hochschule_dto={}", hochschule_dto)
        return hochschule_dto

    def update(
        self, hochschule: Hochschule, hochschule_id: int, version: int
    ) -> HochschuleDTO:
        """Daten einer Hochschule ändern.

        :param hochschule: Die neuen Daten
        :param hochschule_id: ID der zu aktualisierenden Hochschule
        :param version: Version für optimistische Synchronisation
        :return: Die aktualisierte Hochschule
        :rtype: HochschuleDTO
        :raises NotFoundError: Falls die zu aktualisierende Hochschule nicht existiert
        :raises VersionOutdatedError: Falls die Versionsnummer veraltet ist
        :raises NameExistsError: Falls der neue Name bereits vergeben ist
        """
        logger.debug(
            "hochschule_id={}, version={}, {}", hochschule_id, version, hochschule
        )

        with Session() as session:
            if (
                hochschule_db := self.repo.find_by_id(
                    hochschule_id=hochschule_id,
                    session=session,
                )
            ) is None:
                raise NotFoundError(hochschule_id)

            if hochschule_db.version > version:
                raise VersionOutdatedError(version)

            name: Final = hochschule.name
            if name != hochschule_db.name and self.repo.exists_name_other_id(
                hochschule_id=hochschule_id,
                name=name,
                session=session,
            ):
                raise NameExistsError(name)

            hochschule_db.set(hochschule)

            if (
                hochschule_updated := self.repo.update(
                    hochschule=hochschule_db, session=session
                )
            ) is None:
                raise NotFoundError(hochschule_id)

            hochschule_dto: Final = HochschuleDTO.from_hochschule(hochschule_updated)
            logger.debug("{}", hochschule_dto)

            session.commit()
            hochschule_dto.version += 1
            return hochschule_dto

    def delete_by_id(self, hochschule_id: int) -> None:
        """Eine Hochschule anhand ihrer ID löschen.

        :param hochschule_id: ID der zu löschenden Hochschule
        """
        logger.debug("hochschule_id={}", hochschule_id)
        with Session() as session:
            self.repo.delete_by_id(hochschule_id=hochschule_id, session=session)
            session.commit()
