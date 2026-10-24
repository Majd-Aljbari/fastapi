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

"""Unit-Tests für create() von HochschuleWriteService."""

from copy import deepcopy
from datetime import datetime
from typing import Final
from zoneinfo import ZoneInfo

import pytest
lazy from pytest_mock import MockerFixture

from hochschule.entity import Adresse, Hochschule
from hochschule.service import NameExistsError

timezone = ZoneInfo("Europe/Berlin")


@pytest.fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    mocker.patch(
        "hochschule.service.hochschule_write_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda _self: session,
            __exit__=lambda _self, _exc_type, _exc, _tb: None,
        ),
    )
    return session


@pytest.mark.unit
@pytest.mark.unit_create
def test_create(hochschule_write_service, session_mock) -> None:
    # Arrange
    hochschule = Hochschule(
        id=None,
        name="Neue Hochschule",
        homepage="https://www.neue-hs.de",
        version=0,
        adresse=None,
        studenten=[],
        erzeugt=datetime.now(tz=timezone),
        aktualisiert=datetime.now(tz=timezone),
    )
    adresse = Adresse(
        id=None,
        strasse="Teststraße",
        hausnummer="1",
        plz="12345",
        ort="Teststadt",
        hochschule_id=None,
        hochschule=hochschule,
    )
    hochschule.adresse = adresse
    hochschule_db_mock = deepcopy(hochschule)
    generierte_id: Final[int] = 1
    hochschule_db_mock.id = generierte_id
    if hochschule_db_mock.adresse is not None:
        hochschule_db_mock.adresse.id = generierte_id

    # session.scalar(select(func.count()).where(Hochschule.name == name)) → 0
    session_mock.scalar.return_value = 0
    session_mock.add.return_value = None

    def flush_side_effect(objects=None):
        for obj in objects or []:
            obj.id = generierte_id  # Emulation: generierter PK in session.flush()

    session_mock.flush.side_effect = flush_side_effect

    # Act
    hochschule_dto = hochschule_write_service.create(hochschule=hochschule)

    # Assert
    assert hochschule_dto.id == generierte_id


@pytest.mark.unit
@pytest.mark.unit_create
def test_create_name_exists(hochschule_write_service, session_mock) -> None:
    # Arrange
    hochschule = Hochschule(
        id=None,
        name="Hochschule Karlsruhe",
        homepage="https://www.hka.de",
        version=0,
        adresse=None,
        studenten=[],
        erzeugt=datetime.now(tz=timezone),
        aktualisiert=datetime.now(tz=timezone),
    )

    # session.scalar(select(func.count()).where(Hochschule.name == name)) → 1 = Duplikat
    session_mock.scalar.return_value = 1

    # Act
    with pytest.raises(NameExistsError) as err:
        hochschule_write_service.create(hochschule=hochschule)

    # Assert
    assert err.type is NameExistsError
    assert err.value.name == hochschule.name
