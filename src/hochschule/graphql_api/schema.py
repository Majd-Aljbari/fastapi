"""Schema für GraphQL durch Strawberry."""

from dataclasses import asdict
from typing import Final
lazy from collections.abc import Sequence

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.extensions import PydanticErrorExtension
from strawberry.fastapi import GraphQLRouter
lazy from strawberry.types import Info

from hochschule.config.graphql import graphql_ide
from hochschule.graphql_api.graphql_types import (
    CreatePayload,
    HochschuleInput,
    LoginResult,
    Suchparameter,
)
from hochschule.repository import (
    HochschuleRepository,
    HochschuleSuchparameter,
    Pageable,
)
from hochschule.router.hochschule_model import HochschuleModel
from hochschule.security import Role, TokenService
from hochschule.service import (
    HochschuleDTO,
    HochschuleService,
    HochschuleWriteService,
    NotFoundError,
)

__all__ = ["graphql_router"]


_repo: Final = HochschuleRepository()
_service: HochschuleService = HochschuleService(repo=_repo)
# _user_service: UserService = UserService()
_write_service: HochschuleWriteService = HochschuleWriteService(
    repo=_repo,
)
_token_service: Final = TokenService()


@strawberry.type
class Query:
    """Queries, um Hochschuldaten zu lesen."""

    @strawberry.field
    def hochschule(
        self, hochschule_id: strawberry.ID, info: Info
    ) -> HochschuleDTO | None:
        """Daten zu einer Hochschule lesen.

        :param hochschule_id: ID der gesuchten Hochschule
        :return: Gesuchte Hochschule
        :rtype: HochschuleDTO | None
        """
        logger.debug("hochschule_id={}", hochschule_id)

        request: Final[Request] = info.context.get("request")
        user: Final = _token_service.get_user_from_request(request=request)
        if user is None:
            return None

        try:
            hochschule_dto: Final = _service.find_by_id(
                hochschule_id=int(hochschule_id),
                user=user,
            )
        except NotFoundError:
            return None
        logger.debug("{}", hochschule_dto)
        return hochschule_dto

    @strawberry.field
    def hochschulen(
        self,
        suchparameter: Suchparameter | None,
        info: Info,
    ) -> Sequence[HochschuleDTO]:
        """Hochschulen anhand von Suchparametern suchen.

        :param suchparameter: name, ort usw.
        :return: Die gefundenen Hochschulen
        :rtype: list[HochschuleDTO]
        """
        logger.debug("suchparameter={}", suchparameter)

        request: Final[Request] = info.context["request"]
        user: Final = _token_service.get_user_from_request(request)
        if user is None or Role.ADMIN not in user.roles:
            return []

        suchparameter_filtered = (
            None
            if suchparameter is None
            else HochschuleSuchparameter(
                name=suchparameter.name,
            )
        )
        logger.debug("suchparameter_filtered={}", suchparameter_filtered)

        pageable: Final = Pageable.create(size=str(0))
        try:
            hochschulen_dto: Final = _service.find(
                suchparameter=suchparameter_filtered,
                pageable=pageable,
            )
        except NotFoundError:
            return []
        logger.debug("{}", hochschulen_dto)
        return hochschulen_dto.content


@strawberry.type
class Mutation:
    """Mutations, um Hochschuldaten anzulegen, zu ändern oder zu löschen."""

    @strawberry.mutation
    def create(self, hochschule_input: HochschuleInput) -> CreatePayload:
        """Eine neue Hochschule anlegen.

        :param hochschule_input: Daten der neuen Hochschule
        :return: ID der neuen Hochschule
        :rtype: CreatePayload
        """
        logger.debug("hochschule_input={}", hochschule_input)

        hochschule_model: Final = HochschuleModel.model_validate(
            asdict(hochschule_input)
        )

        hochschule_dto: Final = _write_service.create(
            hochschule=hochschule_model.to_hochschule()
        )
        payload: Final = CreatePayload(id=hochschule_dto.id)

        logger.debug("{}", payload)
        return payload

    @strawberry.mutation
    def login(self, username: str, password: str) -> LoginResult:
        """Einen Token zu Benutzername und Passwort ermitteln.

        :param username: Benutzername
        :param password: Passwort
        :rtype: LoginResult
        """
        logger.debug("username={}, password={}", username, password)
        token_mapping = _token_service.token(username=username, password=password)

        token = token_mapping["access_token"]
        user = _token_service.get_user_from_token(token)
        roles: Final = [role.value for role in user.roles]
        return LoginResult(token=token, expires_in="1d", roles=roles)


schema: Final = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        PydanticErrorExtension,
    ],
)


Context = dict[str, Request]


def get_context(request: Request) -> Context:
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema,
    context_getter=get_context,
    graphql_ide=graphql_ide,
)
