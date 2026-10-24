"""HochschuleWriteRouter für Schreib-Operationen (POST, PUT, DELETE)."""

from typing import Annotated, Final

from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response, status
from loguru import logger

from hochschule.problem_details import ProblemDetails
from hochschule.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from hochschule.router.dependencies import get_write_service
from hochschule.router.hochschule_model import HochschuleModel
from hochschule.router.hochschule_update_model import HochschuleUpdateModel
from hochschule.security import Role, RolesRequired
from hochschule.service import HochschuleWriteService, send_mail

__all__ = ["hochschule_write_router"]


hochschule_write_router: Final = APIRouter(tags=["Schreiben"])


@hochschule_write_router.post("")
def post(
    hochschule_model: HochschuleModel,
    request: Request,
    background_tasks: BackgroundTasks,
    service: Annotated[HochschuleWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um eine neue Hochschule anzulegen.

    :param hochschule_model: Hochschuldaten als Pydantic-Model
    :param request: Injiziertes Request-Objekt
    :param background_tasks: Hintergrundtask für den Mailversand
    :param service: Injizierter Service für Geschäftslogik
    """
    logger.debug("hochschule_model={}", hochschule_model)
    hochschule_dto: Final = service.create(
        hochschule=hochschule_model.to_hochschule(),
    )
    logger.debug("hochschule_dto={}", hochschule_dto)

    background_tasks.add_task(send_mail, hochschule_dto)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{hochschule_dto.id}"},
        background=background_tasks,
    )


@hochschule_write_router.put(
    "/{hochschule_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.STUDENT]))],
)
def put(
    hochschule_id: int,
    hochschule_update_model: HochschuleUpdateModel,
    request: Request,
    service: Annotated[HochschuleWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um eine Hochschule zu aktualisieren.

    :param hochschule_id: ID der zu aktualisierenden Hochschule
    :param request: Injiziertes Request-Objekt mit If-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    """
    if_match_value: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "hochschule_id={}, if_match={}, hochschule_update_model={}",
        hochschule_id,
        if_match_value,
        hochschule_update_model,
    )

    if if_match_value is None:
        return ProblemDetails.create(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        ).to_response()

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return ProblemDetails.create(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        ).to_response()

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    hochschule: Final = hochschule_update_model.to_hochschule()
    hochschule_modified: Final = service.update(
        hochschule=hochschule,
        hochschule_id=hochschule_id,
        version=version_int,
    )
    logger.debug("hochschule_modified={}", hochschule_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{hochschule_modified.version}"'},
    )


@hochschule_write_router.delete(
    "/{hochschule_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.STUDENT]))],
)
def delete_by_id(
    hochschule_id: int,
    service: Annotated[HochschuleWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um eine Hochschule anhand ihrer ID zu löschen.

    :param hochschule_id: ID der zu löschenden Hochschule
    :param service: Injizierter Service für Geschäftslogik
    """
    logger.debug("hochschule_id={}", hochschule_id)
    service.delete_by_id(hochschule_id=hochschule_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
