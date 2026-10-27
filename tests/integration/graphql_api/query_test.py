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

"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

import pytest
from common_api_test import certificate_path, graphql_url, login_graphql, timeout
from requests import post


@pytest.mark.graphql
@pytest.mark.query
def test_query_id() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                hochschule(hochschuleId: "1000") {
                    version
                    name
                    homepage
                    adresse {
                        plz
                        ort
                    }
                    studenten {
                        matrikelnummer
                        vorname
                        nachname
                        email
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(
        graphql_url,
        json=query,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    data: Final = response_body["data"]
    assert data is not None
    hochschule: Final = data["hochschule"]
    assert isinstance(hochschule, dict)
    assert response_body.get("errors") is None


@pytest.mark.graphql
@pytest.mark.query
def test_query_id_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                hochschule(hochschuleId: "999999") {
                    name
                }
            }
        """,
    }

    # act
    response: Final = post(
        graphql_url,
        json=query,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"]["hochschule"] is None
    assert response_body.get("errors") is None


@pytest.mark.graphql
@pytest.mark.query
def test_query_name() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                hochschulen(suchparameter: {name: "Hochschule Karlsruhe"}) {
                    id
                    version
                    name
                    homepage
                }
            }
        """,
    }

    # act
    response: Final = post(
        graphql_url,
        json=query,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    hochschulen: Final = response_body["data"]["hochschulen"]
    assert isinstance(hochschulen, list)
    assert len(hochschulen) > 0
    assert response_body.get("errors") is None


@pytest.mark.graphql
@pytest.mark.query
def test_query_name_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                hochschulen(suchparameter: {name: "NichtVorhandenXYZ"}) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(
        graphql_url,
        json=query,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    hochschulen: Final = response_body["data"]["hochschulen"]
    assert isinstance(hochschulen, list)
    assert len(hochschulen) == 0
