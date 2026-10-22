"""HochschuleGetRouter für Lese-Operationen."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Query, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from hochschule.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from hochschule.router.dependencies import get_service
from hochschule.router.hochschule_find_model import (
    HochschuleFindModel,
    HochschulePageModel,
    HochschuleResponseModel,
)
from hochschule.security import Role, RolesRequired, User
from hochschule.service import HochschuleService

__all__ = ["hochschule_router"]


hochschule_router: Final = APIRouter(tags=["Lesen"])


@hochschule_router.get(
    path="/{hochschule_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.STUDENT]))],
    response_model=HochschuleResponseModel,
)
def get_by_id(
    hochschule_id: int,
    request: Request,
    service: Annotated[HochschuleService, Depends(get_service)],
) -> Response:
    """Suche mit der Hochschule-ID.

    :param hochschule_id: ID der gesuchten Hochschule als Pfadparameter
    :param request: Injiziertes Request-Objekt von FastAPI
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit dem gefundenen Hochschuldatensatz
    """
    user: Final[User] = request.state.current_user
    logger.debug("hochschule_id={}, user={}", hochschule_id, user)

    hochschule: Final = service.find_by_id(hochschule_id=hochschule_id, user=user)
    logger.debug("{}", hochschule)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)
        if version is not None:
            try:
                if int(version) == hochschule.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                logger.debug("invalid version={}", version)

    hochschule_model: Final = HochschuleResponseModel.from_dto(hochschule)
    return JSONResponse(
        content=hochschule_model.model_dump(mode="json"),
        headers={ETAG: f'"{hochschule.version}"'},
    )


@hochschule_router.get(
    path="",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
    response_model=HochschulePageModel,
)
def get(
    find_model: Annotated[HochschuleFindModel, Query()],
    service: Annotated[HochschuleService, Depends(get_service)],
) -> HochschulePageModel:
    """Suche mit Query-Parameter.

    :param find_model: Validierte Such- und Pagination-Parameter
    :param service: Injizierter Service für Geschäftslogik
    :return: Eine Seite mit Hochschul-Daten
    """
    logger.debug("search={}", find_model)
    result: Final = _find_page(service=service, find_model=find_model)
    logger.debug("result={}", result)
    return result


@hochschule_router.api_route(
    path="/query",
    methods=["QUERY"],
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
    response_model=HochschulePageModel,
)
def query(
    find_model: HochschuleFindModel,
    service: Annotated[HochschuleService, Depends(get_service)],
) -> HochschulePageModel:
    """Suche mit HTTP-Methode QUERY im Request-Body.

    :param find_model: Validierte Suchparameter aus dem Request-Body
    :param service: Injizierter Service für Geschäftslogik
    :return: Eine Seite mit Hochschul-Daten
    """
    logger.debug("search={}", find_model)
    result: Final = _find_page(service=service, find_model=find_model)
    logger.debug("result={}", result)
    return result


@hochschule_router.get(
    path="/namen/{teil}",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
    response_model=list[str],
)
def get_namen(
    teil: str,
    service: Annotated[HochschuleService, Depends(get_service)],
) -> list[str]:
    """Suche Hochschulnamen zum gegebenen Teilstring.

    :param teil: Teilstring der gesuchten Namen
    :param service: Injizierter Service für Geschäftslogik
    :return: Liste der gefundenen Hochschulnamen
    """
    logger.debug("teil={}", teil)
    namen: Final = service.find_namen(teil=teil)
    return list(namen)


def _find_page(
    service: HochschuleService,
    find_model: HochschuleFindModel,
) -> HochschulePageModel:
    pageable: Final = find_model.to_pageable()
    hochschule_slice: Final = service.find(
        suchparameter=find_model.to_suchparameter(),
        pageable=pageable,
    )

    hochschule_models: Final = tuple(
        HochschuleResponseModel.from_dto(hs) for hs in hochschule_slice.content
    )

    total_pages: Final = (
        (hochschule_slice.total_elements + pageable.size - 1) // pageable.size
        if pageable.size > 0
        else 1
    )

    return HochschulePageModel(
        content=hochschule_models,
        page={
            "size": pageable.size,
            "number": pageable.number,
            "total_elements": hochschule_slice.total_elements,
            "total_pages": total_pages,
        },
    )
