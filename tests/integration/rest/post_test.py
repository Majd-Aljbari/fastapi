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

"""Tests für POST."""

from http import HTTPStatus
from re import search
from typing import Final

import pytest
from common_api_test import certificate_path, rest_url, timeout
from requests import post


@pytest.mark.rest
@pytest.mark.post_request
@pytest.mark.post_request_success
def test_post() -> None:
    # arrange
    neue_hochschule: Final = {
        "name": "Neue Testuniversität",
        "homepage": "https://www.test-uni.de",
        "adresse": {
            "strasse": "Teststraße",
            "hausnummer": "1",
            "plz": "12345",
            "ort": "Teststadt",
        },
        "studenten": [],
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neue_hochschule,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "/[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@pytest.mark.rest
@pytest.mark.post_request
def test_post_invalid() -> None:
    # arrange
    neue_hochschule_invalid: Final = {
        "name": "X",
        "homepage": "kein-url",
        "adresse": {
            "strasse": "Teststraße",
            "hausnummer": "1",
            "plz": "123",
            "ort": "Teststadt",
        },
    }
    headers = {"Content-Type": "application/json"}

    # act
    try:
        response: Final = post(
            rest_url,
            json=neue_hochschule_invalid,
            headers=headers,
            timeout=timeout,
            verify=certificate_path,
        )
    except BaseException as exc:
        raise RuntimeError("Fehler bei POST") from exc

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.rest
@pytest.mark.post_request
def test_post_name_exists() -> None:
    # arrange
    name_exists: Final = "Hochschule Karlsruhe"
    neue_hochschule: Final = {
        "name": name_exists,
        "homepage": "https://www.test.de",
        "adresse": {
            "strasse": "Moltkestraße",
            "hausnummer": "30",
            "plz": "76133",
            "ort": "Karlsruhe",
        },
        "studenten": [],
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neue_hochschule,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert name_exists in response.text


@pytest.mark.rest
@pytest.mark.post_request
def test_post_invalid_json() -> None:
    # arrange
    json_invalid: Final = '{"name" "TestHochschule"}'
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=json_invalid,
        headers=headers,
        timeout=timeout,
        verify=certificate_path,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "should be a valid dictionary" in response.text
