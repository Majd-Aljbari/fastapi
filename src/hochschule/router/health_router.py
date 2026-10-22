"""HealthRouter zur Überprüfung des Systemstatus."""

from typing import Final

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from hochschule.repository import engine

__all__ = ["router"]

router: Final = APIRouter(tags=["Health"])


@router.get("/liveness")
def liveness() -> dict[str, str]:
    """Überprüfen der Liveness.

    :return: JSON-Datensatz mit der Statusmeldung
    """
    return {"status": "up"}


@router.get("/readiness")
def readiness() -> dict[str, str]:
    """Überprüfen der Readiness (Datenbankverbindung).

    :return: JSON-Datensatz mit der Statusmeldung
    """
    with engine.connect() as connection:
        try:
            connection.scalar(text("SELECT 1"))
        except OperationalError:
            return {"db": "down"}
    return {"db": "up"}
