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

"""Geschäftslogik zum Lesen von Hochschuldaten."""

from datetime import datetime
from typing import Final
from zoneinfo import ZoneInfo
lazy from collections.abc import Sequence

from loguru import logger
from openpyxl import Workbook

from hochschule.config import excel_enabled
from hochschule.repository import (
    HochschuleRepository,
    HochschuleSuchparameter,
    Pageable,
    Session,
    Slice,
)
from hochschule.service.exceptions import NotFoundError
from hochschule.service.hochschule_dto import HochschuleDTO

__all__ = ["HochschuleService"]


class HochschuleService:
    """Service-Klasse mit Geschäftslogik für Hochschule."""

    def __init__(self, repo: HochschuleRepository) -> None:
        """Konstruktor mit abhängigem HochschuleRepository."""
        self.repo: HochschuleRepository = repo

    def find_by_id(self, hochschule_id: int) -> HochschuleDTO:
        """Suche mit der Hochschul-ID.

        :param hochschule_id: ID für die Suche
        :return: Die gefundene Hochschule
        :rtype: HochschuleDTO
        :raises NotFoundError: Falls keine Hochschule gefunden wurde
        """
        logger.debug("hochschule_id={}", hochschule_id)

        with Session() as session:
            if (
                hochschule := self.repo.find_by_id(
                    session=session,
                    hochschule_id=hochschule_id,
                )
            ) is None:
                message: Final = f"Keine Hochschule mit der ID {hochschule_id}"
                logger.debug("NotFoundError: {}", message)
                raise NotFoundError(patient_id=hochschule_id)

            hochschule_dto: Final = HochschuleDTO.from_hochschule(hochschule)
            session.commit()

        logger.debug("{}", hochschule_dto)
        return hochschule_dto

    def find(
        self,
        suchparameter: HochschuleSuchparameter | None,
        pageable: Pageable,
    ) -> Slice[HochschuleDTO]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter oder None
        :param pageable: Anzahl Datensätze und Seitennummer
        :return: Slice der gefundenen Hochschulen
        :rtype: Slice[HochschuleDTO]
        :raises NotFoundError: Falls keine Hochschulen gefunden wurden
        """
        logger.debug("{}", suchparameter)
        with Session() as session:
            hochschule_slice: Final = self.repo.find(
                suchparameter=suchparameter,
                pageable=pageable,
                session=session,
            )
            if len(hochschule_slice.content) == 0:
                raise NotFoundError(suchparameter=suchparameter)

            hochschulen_dto: Final = tuple(
                HochschuleDTO.from_hochschule(h) for h in hochschule_slice.content
            )
            session.commit()

        if excel_enabled:
            self._create_excelsheet(hochschulen_dto)
        hochschulen_dto_slice = Slice(
            content=hochschulen_dto,
            total_elements=hochschule_slice.total_elements,
        )
        logger.debug("{}", hochschulen_dto_slice)
        return hochschulen_dto_slice

    def find_namen(self, teil: str) -> Sequence[str]:
        """Suche Namen zu einem Teilstring.

        :param teil: Teilstring der gesuchten Namen
        :return: Liste der gefundenen Namen oder eine leere Liste
        :rtype: Sequence[str]
        :raises NotFoundError: Falls keine Namen gefunden wurden
        """
        logger.debug("teil={}", teil)
        with Session() as session:
            namen: Final = self.repo.find_namen(teil=teil, session=session)
            session.commit()

        logger.debug("{}", namen)
        if len(namen) == 0:
            raise NotFoundError
        return namen

    def _create_excelsheet(self, hochschulen: tuple[HochschuleDTO, ...]) -> None:
        """Ein Excelsheet mit den gefundenen Hochschulen erstellen.

        :param hochschulen: Hochschuldaten für das Excelsheet
        """
        workbook: Final = Workbook()
        worksheet: Final = workbook.active
        if worksheet is None:
            return

        worksheet.append(["Name", "Homepage"])
        for hochschule in hochschulen:
            worksheet.append((
                hochschule.name,
                hochschule.homepage or "N/A",
            ))

        timestamp: Final = datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime(
            format="%Y-%m-%d_%H%M%S",
        )
        workbook.save(f"hochschulen-{timestamp}.xlsx")
