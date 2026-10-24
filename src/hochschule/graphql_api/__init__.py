"""Modul für die GraphQL-Schnittstelle."""

from hochschule.graphql_api.graphql_types import (
    AdresseInput,
    CreatePayload,
    HochschuleInput,
    Suchparameter,
)
from hochschule.graphql_api.schema import Mutation, Query, graphql_router

__all__ = [
    "AdresseInput",
    "CreatePayload",
    "HochschuleInput",
    "Mutation",
    "Query",
    "Suchparameter",
    "graphql_router",
]
