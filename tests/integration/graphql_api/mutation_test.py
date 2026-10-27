# Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Tests für Mutations mit GraphQL."""

from http import HTTPStatus
from typing import Final

import pytest
from common_api_test import certificate_path, graphql_url, timeout
from requests import post


@pytest.mark.graphql
@pytest.mark.mutation
def test_create() -> None:
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    hochschuleInput: {
                        name: "GraphQL Testuniversität"
                        homepage: "https://graphql-test.de"
                        adresse: {
                            strasse: "Teststraße"
                            hausnummer: "1"
                            plz: "12345"
                            ort: "Teststadt"
                        }
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(
        graphql_url,
        json=query,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response is not None
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body.get("errors") is None
    assert isinstance(response_body["data"]["create"]["id"], int)


@pytest.mark.graphql
@pytest.mark.mutation
def test_create_invalid() -> None:
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    hochschuleInput: {
                        name: "X"
                        homepage: "kein-url"
                        adresse: {
                            strasse: "Teststraße"
                            hausnummer: "1"
                            plz: "123"
                            ort: "Teststadt"
                        }
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(
        graphql_url,
        json=query,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    errors: Final = response_body.get("errors")
    assert errors is not None
    assert len(errors) > 0
