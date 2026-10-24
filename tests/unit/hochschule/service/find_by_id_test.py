# ruff: file-ignore[hardcoded-password-func-arg]
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

"""Unit-Tests für find_by_id() von HochschuleService."""

from dataclasses import asdict
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
lazy from pytest_mock import MockerFixture

from hochschule.entity import Adresse, Hochschule
from hochschule.security import Role, User
from hochschule.service import (
    ForbiddenError,
    HochschuleDTO,
    HochschuleService,
    NotFoundError,
)

timezone = ZoneInfo("Europe/Berlin")


@pytest.fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    mocker.patch(
        "hochschule.service.hochschule_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda _self: session,
            __exit__=lambda _self, _exc_type, _exc, _tb: None,
        ),
    )
    return session


@pytest.mark.unit
@pytest.mark.unit_find_by_id
def test_find_by_id(hochschule_service, session_mock) -> None:
    # Arrange
    hochschule_id = 1
    hochschule_mock = Hochschule(
        id=hochschule_id,
        name="Hochschule Karlsruhe",
        homepage="https://www.hka.de",
        version=0,
        adresse=None,
        studenten=[],
        erzeugt=datetime.now(tz=timezone),
        aktualisiert=datetime.now(tz=timezone),
    )
    adresse_mock = Adresse(
        id=11,
        strasse="Moltkestraße",
        hausnummer="30",
        plz="76133",
        ort="Karlsruhe",
        hochschule_id=hochschule_id,
        hochschule=hochschule_mock,
    )
    hochschule_mock.adresse = adresse_mock
    user_mock = User(
        username="admin",
        email="admin@hka.de",
        nachname="Admin",
        vorname="Admin",
        roles=[Role.ADMIN],
        password="mockpass",
    )
    hochschule_dto_mock = HochschuleDTO.from_hochschule(hochschule_mock)
    # session.scalar(select(Hochschule)...)
    session_mock.scalar.return_value = hochschule_mock

    # Act
    hochschule_dto = hochschule_service.find_by_id(
        hochschule_id=hochschule_id, user=user_mock
    )

    # Assert
    assert asdict(hochschule_dto) == asdict(hochschule_dto_mock)


@pytest.mark.unit
@pytest.mark.unit_find_by_id
def test_find_by_id_not_found(
    hochschule_service: HochschuleService, session_mock
) -> None:
    # Arrange
    hochschule_id = 999
    user_mock = User(
        username="admin",
        email="admin@hka.de",
        nachname="Admin",
        vorname="Admin",
        roles=[Role.ADMIN],
        password="mockpass",
    )
    # session.scalar(select(Hochschule)...)
    session_mock.scalar.return_value = None

    # Act
    with pytest.raises(NotFoundError) as err:
        hochschule_service.find_by_id(hochschule_id=hochschule_id, user=user_mock)

    # Assert
    assert err.type == NotFoundError
    assert str(err.value) == "Not Found"
    assert err.value.hochschule_id == hochschule_id


@pytest.mark.unit
@pytest.mark.unit_find_by_id
def test_find_by_id_not_found_not_admin(
    hochschule_service: HochschuleService,
    session_mock,
) -> None:
    # Arrange
    hochschule_id = 999
    user_mock = User(
        username="student",
        email="student@hka.de",
        nachname="Student",
        vorname="Student",
        roles=[],
        password="mockpass",
    )
    # session.scalar(select(Hochschule)...)
    session_mock.scalar.return_value = None

    # Act
    with pytest.raises(ForbiddenError) as err:
        hochschule_service.find_by_id(hochschule_id=hochschule_id, user=user_mock)

    # Assert
    assert err.type == ForbiddenError


@pytest.mark.unit
@pytest.mark.unit_find_by_id
def test_find_by_id_student(hochschule_service, session_mock) -> None:
    # Arrange
    hochschule_id = 1
    hochschule_mock = Hochschule(
        id=hochschule_id,
        name="Hochschule Karlsruhe",
        homepage="https://www.hka.de",
        version=0,
        adresse=None,
        studenten=[],
        erzeugt=datetime.now(tz=timezone),
        aktualisiert=datetime.now(tz=timezone),
    )
    user_mock = User(
        username="student",
        email="student@hka.de",
        nachname="Student",
        vorname="Student",
        roles=[Role.STUDENT],
        password="mockpass",
    )
    hochschule_dto_mock = HochschuleDTO.from_hochschule(hochschule_mock)
    # session.scalar(select(Hochschule)...)
    session_mock.scalar.return_value = hochschule_mock

    # Act
    hochschule_dto = hochschule_service.find_by_id(
        hochschule_id=hochschule_id, user=user_mock
    )

    # Assert
    assert asdict(hochschule_dto) == asdict(hochschule_dto_mock)
