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

"""Tests für QUERY."""

from http import HTTPStatus
from typing import Final

import pytest
from common_api_test import certificate_path, login, rest_url, timeout
from requests import request

QUERY_METHOD: Final = "QUERY"
QUERY_URL: Final = f"{rest_url}/query"


@pytest.mark.rest
@pytest.mark.query_request
@pytest.mark.parametrize("name", ["Hochschule Karlsruhe", "Hochschule Pforzheim"])
def test_get_by_name(name: str) -> None:
    # arrange
    params = {"name": name}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = request(
        method=QUERY_METHOD,
        url=QUERY_URL,
        json=params,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) == 1
    hochschule = content[0]
    assert hochschule is not None
    assert hochschule.get("name") == name
    assert hochschule.get("id") is not None


@pytest.mark.rest
@pytest.mark.query_request
@pytest.mark.parametrize("name", ["NichtVorhanden", "FooBar Hochschule"])
def test_get_by_name_not_found(name: str) -> None:
    # arrange
    params = {"name": name}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = request(
        method=QUERY_METHOD,
        url=QUERY_URL,
        json=params,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.rest
@pytest.mark.query_request
@pytest.mark.parametrize("teil", ["Hochschule", "a"])
def test_get_by_name_teil(teil: str) -> None:
    # arrange
    params = {"name": teil}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = request(
        method=QUERY_METHOD,
        url=QUERY_URL,
        json=params,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body["content"]
    for hs in content:
        name = hs.get("name")
        assert name is not None
        assert isinstance(name, str)
        assert teil.lower() in name.lower()
        assert hs.get("id") is not None
