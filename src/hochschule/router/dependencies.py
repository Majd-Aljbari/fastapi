"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from hochschule.repository.hochschule_repository import HochschuleRepository
from hochschule.security.dependencies import get_user_service
from hochschule.security.user_service import UserService
from hochschule.service.hochschule_service import HochschuleService
from hochschule.service.hochschule_write_service import HochschuleWriteService


def get_repository() -> HochschuleRepository:
    """Factory-Funktion für HochschuleRepository.

    :return: Das Repository
    :rtype: HochschuleRepository
    """
    return HochschuleRepository()


def get_service(
    repo: Annotated[HochschuleRepository, Depends(get_repository)],
) -> HochschuleService:
    """Factory-Funktion für HochschuleService."""
    return HochschuleService(repo=repo)


# def get_write_service(
#     repo: Annotated[HochschuleRepository, Depends(get_repository)],
#     user_service: Annotated[UserService, Depends(get_user_service)],
# ) -> HochschuleWriteService:
#     """Factory-Funktion für HochschuleWriteService."""
#     return HochschuleWriteService(repo=repo, user_service=user_service)
def get_write_service(
    repo: Annotated[HochschuleRepository, Depends(get_repository)],
) -> HochschuleWriteService:
    """Factory-Funktion für HochschuleWriteService."""
    return HochschuleWriteService(repo=repo)
