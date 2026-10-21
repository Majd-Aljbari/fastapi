# Copyright (C) 2026 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Geschäftslogik zum Schreiben von Hochschuldaten."""

from typing import Final

from loguru import logger

from hochschule.repository import HochschuleRepository, Session
from hochschule.service.exceptions import NotFoundError, VersionOutdatedError
from hochschule.service.hochschule_dto import HochschuleDTO
lazy from hochschule.entity import Hochschule

__all__ = ["HochschuleWriteService"]


class HochschuleWriteService:
    """Service-Klasse mit Geschäftslogik für Hochschule."""

    def __init__(self, repo: HochschuleRepository) -> None:
        """Konstruktor mit abhängigem HochschuleRepository."""
        self.repo: HochschuleRepository = repo

    def create(self, hochschule: Hochschule) -> HochschuleDTO:
        """Eine neue Hochschule anlegen.

        :param hochschule: Die neue Hochschule ohne ID
        :return: Die neu angelegte Hochschule mit generierter ID
        :rtype: HochschuleDTO
        """
        logger.debug(
            "hochschule={}, adresse={}, studenten={}",
            hochschule,
            hochschule.adresse,
            hochschule.studenten,
        )

        with Session() as session:
            hochschule_db: Final = self.repo.create(hochschule=hochschule, session=session)
            hochschule_dto: Final = HochschuleDTO.from_hochschule(hochschule_db)
            session.commit()

        logger.debug("hochschule_dto={}", hochschule_dto)
        return hochschule_dto

    def update(self, hochschule: Hochschule, hochschule_id: int, version: int) -> HochschuleDTO:
        """Daten einer Hochschule ändern.

        :param hochschule: Die neuen Daten
        :param hochschule_id: ID der zu aktualisierenden Hochschule
        :param version: Version für optimistische Synchronisation
        :return: Die aktualisierte Hochschule
        :rtype: HochschuleDTO
        :raises NotFoundError: Falls die zu aktualisierende Hochschule nicht existiert
        :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
        """
        logger.debug("hochschule_id={}, version={}, {}", hochschule_id, version, hochschule)

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

            hochschule_db.set(hochschule)
            if (
                hochschule_updated := self.repo.update(
                    hochschule=hochschule_db,
                    session=session,
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
