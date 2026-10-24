"""Repository fuer persistente Hochschuldaten."""

from collections.abc import Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from hochschule.entity import Hochschule
from hochschule.repository.hochschule_suchparameter import HochschuleSuchparameter
from hochschule.repository.pageable import Pageable
from hochschule.repository.slice import Slice

__all__ = ["HochschuleRepository"]


class HochschuleRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Hochschule."""

    def find_by_id(
        self, hochschule_id: int | None, session: Session
    ) -> Hochschule | None:
        """Suche mit der Hochschule-ID.

        :param hochschule_id: ID der gesuchten Hochschule
        :param session: Session für SQLAlchemy
        :return: Die gefundene Hochschule oder None
        :rtype: Hochschule | None
        """
        logger.debug("hochschule_id={}", hochschule_id)

        if hochschule_id is None:
            return None

        statement: Final = (
            select(Hochschule)
            .options(
                joinedload(Hochschule.adresse),
                selectinload(Hochschule.studenten),
            )
            .where(Hochschule.id == hochschule_id)
        )
        hochschule: Final = session.scalar(statement)

        logger.debug("{}", hochschule)
        return hochschule

    def find(
        self,
        suchparameter: HochschuleSuchparameter | None,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Hochschule]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter oder None
        :param pageable: Anzahl Datensätze und Seitennummer
        :param session: Session für SQLAlchemy
        :return: Slice der gefundenen Hochschulen
        :rtype: Slice[Hochschule]
        """
        log_str: Final = "{}"
        logger.debug(log_str, suchparameter)
        if suchparameter is None or suchparameter.is_empty():
            return self._find_all(pageable=pageable, session=session)

        if suchparameter.name is not None:
            hochschulen = self._find_by_name(
                teil=suchparameter.name,
                pageable=pageable,
                session=session,
            )
            logger.debug(log_str, hochschulen)
            return hochschulen

        return Slice(content=(), total_elements=0)

    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Hochschule]:
        logger.debug("aufgerufen")
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Hochschule)
                .options(
                    joinedload(Hochschule.adresse),
                    selectinload(Hochschule.studenten),
                )
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Hochschule).options(
                    joinedload(Hochschule.adresse),
                    selectinload(Hochschule.studenten),
                )
            )
        )
        hochschulen: Final = (session.scalars(statement)).all()
        anzahl: Final = self._count_all_rows(session)
        hochschule_slice: Final = Slice(
            content=tuple(hochschulen), total_elements=anzahl
        )
        logger.debug("hochschule_slice={}", hochschule_slice)
        return hochschule_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Hochschule)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_name(
        self,
        teil: str,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Hochschule]:
        logger.debug("teil={}", teil)
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Hochschule)
                .options(
                    joinedload(Hochschule.adresse),
                    selectinload(Hochschule.studenten),
                )
                .filter(Hochschule.name.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Hochschule)
                .options(
                    joinedload(Hochschule.adresse),
                    selectinload(Hochschule.studenten),
                )
                .filter(Hochschule.name.ilike(f"%{teil}%"))
            )
        )
        hochschulen: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_name(teil, session)
        hochschule_slice: Final = Slice(
            content=tuple(hochschulen), total_elements=anzahl
        )
        logger.debug("{}", hochschule_slice)
        return hochschule_slice

    def _count_rows_name(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Hochschule)
            .filter(Hochschule.name.ilike(f"%{teil}%"))
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def exists_name(self, name: str, session: Session) -> bool:
        """Abfrage, ob es den Hochschulnamen bereits gibt.

        :param name: Name der Hochschule
        :param session: Session für SQLAlchemy
        :return: True, falls es den Namen bereits gibt, False sonst
        :rtype: bool
        """
        logger.debug("name={}", name)

        statement: Final = select(func.count()).where(Hochschule.name == name)
        anzahl: Final = session.scalar(statement)
        logger.debug("anzahl={}", anzahl)
        return anzahl is not None and anzahl > 0

    def exists_name_other_id(
        self,
        name: str,
        hochschule_id: int,
        session: Session,
    ) -> bool:
        """Abfrage, ob es den Hochschulnamen bei einer anderen Hochschule-ID bereits gibt.

        :param name: Name der Hochschule
        :param hochschule_id: eigene Hochschule-ID
        :param session: Session für SQLAlchemy
        :return: True, falls es den Namen bereits gibt, False sonst
        :rtype: bool
        """
        logger.debug("name={}", name)

        statement: Final = select(Hochschule.id).where(Hochschule.name == name)
        id_db: Final = session.scalar(statement)
        logger.debug("id_db={}", id_db)
        return id_db is not None and id_db != hochschule_id

    def create(self, hochschule: Hochschule, session: Session) -> Hochschule:
        """Speichere eine neue Hochschule ab.

        :param hochschule: Die Daten der neuen Hochschule ohne ID
        :param session: Session für SQLAlchemy
        :return: Die neu angelegte Hochschule mit generierter ID
        :rtype: Hochschule
        """
        logger.debug(
            "hochschule={}, hochschule.adresse={}, hochschule.studenten={}",
            hochschule,
            hochschule.adresse,
            hochschule.studenten,
        )
        session.add(instance=hochschule)
        session.flush(objects=[hochschule])
        logger.debug("hochschule_id={}", hochschule.id)
        return hochschule

    def update(self, hochschule: Hochschule, session: Session) -> Hochschule | None:
        """Aktualisiere eine Hochschule.

        :param hochschule: Die neuen Hochschuldaten
        :param session: Session für SQLAlchemy
        :return: Die aktualisierte Hochschule oder None, falls kein Eintrag mit der ID existiert
        :rtype: Hochschule | None
        """
        logger.debug("{}", hochschule)

        if (
            hochschule_db := self.find_by_id(
                hochschule_id=hochschule.id, session=session
            )
        ) is None:
            return None

        logger.debug("{}", hochschule_db)
        return hochschule_db

    def delete_by_id(self, hochschule_id: int, session: Session) -> None:
        """Lösche die Daten zu einer Hochschule.

        :param hochschule_id: Die ID der zu löschenden Hochschule
        :param session: Session für SQLAlchemy
        """
        logger.debug("hochschule_id={}", hochschule_id)

        if (
            hochschule := self.find_by_id(
                hochschule_id=hochschule_id, session=session
            )
        ) is None:
            return
        session.delete(hochschule)
        logger.debug("ok")

    def find_namen(self, teil: str, session: Session) -> Sequence[str]:
        """Suche Hochschulnamen zu einem Teilstring.

        :param teil: Teilstring zu den gesuchten Namen
        :param session: Session für SQLAlchemy
        :return: Liste der gefundenen Namen oder eine leere Liste
        :rtype: Sequence[str]
        """
        logger.debug("teil={}", teil)

        statement: Final = (
            select(Hochschule.name)
            .filter(Hochschule.name.ilike(f"%{teil}%"))
            .distinct()
        )
        namen: Final = (session.scalars(statement)).all()

        logger.debug("namen={}", namen)
        return namen
