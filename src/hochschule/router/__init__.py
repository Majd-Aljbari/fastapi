"""Modul für die REST-Schnittstelle einschließlich Validierung."""

lazy from collections.abc import Sequence

from hochschule.router.health_router import liveness, readiness, router as health_router
from hochschule.router.hello_router import router as hello_router
from hochschule.router.hochschule_router import (
    get,
    get_by_id,
    get_namen,
    hochschule_router,
    query,
)
from hochschule.router.hochschule_write_router import (
    delete_by_id,
    hochschule_write_router,
    post,
    put,
)
from hochschule.router.shutdown_router import router as shutdown_router, shutdown

__all__: Sequence[str] = [
    "delete_by_id",
    "get",
    "get_by_id",
    "get_namen",
    "health_router",
    "hello_router",
    "hochschule_router",
    "hochschule_write_router",
    "liveness",
    "post",
    "put",
    "query",
    "readiness",
    "shutdown",
    "shutdown_router",
]
