"""Geschäftslogik zum Lesen von Hochschuldaten."""

from collections.abc import Sequence
from datetime import datetime
from typing import Final
from zoneinfo import ZoneInfo

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
from hochschule.security import Role, User
from hochschule.service.exceptions import ForbiddenError, NotFoundError
from hochschule.service.hochschule_dto import HochschuleDTO

__all__ = ["HochschuleService"]


class HochschuleService:
    """Service-Klasse mit Geschäftslogik für Lese-Operationen bei Hochschule."""

    def __init__(self, repo: HochschuleRepository) -> None:
        """Konstruktor mit abhängigem HochschuleRepository."""
        self.repo: HochschuleRepository = repo

    def find_by_id(self, hochschule_id: int, user: User) -> HochschuleDTO:
        """Suche mit der Hochschule-ID.

        :param hochschule_id: ID für die Suche
        :param user: User aus dem Authentifizierungs-Token
        :return: Die gefundene Hochschule
        :rtype: HochschuleDTO
        :raises NotFoundError: Falls keine Hochschule gefunden wurde
        :raises ForbiddenError: Falls die Hochschuldaten nicht gelesen werden dürfen
        """
        logger.debug("hochschule_id={}, user={}", hochschule_id, user)

        with Session() as session:
            user_is_admin: Final = Role.ADMIN in user.roles

            if (
                hochschule := self.repo.find_by_id(
                    session=session, hochschule_id=hochschule_id
                )
            ) is None:
                if user_is_admin:
                    message: Final = f"Keine Hochschule mit der ID {hochschule_id}"
                    logger.debug("NotFoundError: {}", message)
                    raise NotFoundError(hochschule_id=hochschule_id)
                logger.debug("nicht admin")
                raise ForbiddenError

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
        :param pageable: Pagination-Informationen
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
                HochschuleDTO.from_hochschule(hochschule)
                for hochschule in hochschule_slice.content
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
        """Suche Hochschulnamen zu einem Teilstring.

        :param teil: Teilstring der gesuchten Namen
        :return: Liste der gefundenen Namen
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

        worksheet.append(["ID", "Name", "Homepage", "Ort"])
        for hs in hochschulen:
            ort = hs.adresse.ort if hs.adresse is not None else "N/A"
            homepage = hs.homepage if hs.homepage is not None else "N/A"
            worksheet.append((hs.id, hs.name, homepage, ort))

        timestamp: Final = datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime(
            format="%Y-%m-%d_%H%M%S",
        )
        workbook.save(f"hochschulen-{timestamp}.xlsx")
