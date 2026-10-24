"""REST-Schnittstelle für Shutdown."""

import os
import signal
from typing import Any, Final

from fastapi import APIRouter, Depends
from loguru import logger

from hochschule.security.role import Role
from hochschule.security.roles_required import RolesRequired

__all__ = ["router"]

router: Final = APIRouter(tags=["Admin"])


@router.api_route(
    path="/shutdown",
    methods=["QUERY"],
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def shutdown() -> dict[str, Any]:
    """Der Server wird heruntergefahren."""
    logger.warning("Server shutting down without calling cleanup handlers.")
    os.kill(os.getpid(), signal.SIGINT)
    return {"message": "Server is shutting down..."}
