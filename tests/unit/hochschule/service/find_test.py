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

"""Unit-Tests für find() von HochschuleService."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
lazy from pytest_mock import MockerFixture

from hochschule.entity import Hochschule
from hochschule.repository import HochschuleSuchparameter, Pageable
from hochschule.service import NotFoundError

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
@pytest.mark.unit_find
def test_find_by_name(hochschule_service, session_mock) -> None:
    # Arrange
    name = "Hochschule Karlsruhe"
    hochschule_id = 1
    hochschule_mock = Hochschule(
        id=hochschule_id,
        name=name,
        homepage="https://www.hka.de",
        version=0,
        adresse=None,
        studenten=[],
        erzeugt=datetime.now(tz=timezone),
        aktualisiert=datetime.now(tz=timezone),
    )
    suchparameter = HochschuleSuchparameter(name=name)
    pageable = Pageable(size=5, number=0)
    # session.scalars(select(Hochschule)...).all()
    session_mock.scalars.return_value.all.return_value = [hochschule_mock]

    # Act
    hochschulen_slice = hochschule_service.find(
        suchparameter=suchparameter,
        pageable=pageable,
    )

    # Assert
    assert len(hochschulen_slice.content) == 1
    assert hochschulen_slice.content[0].name == name


@pytest.mark.unit
@pytest.mark.unit_find
def test_find_by_name_not_found(hochschule_service, session_mock) -> None:
    # Arrange
    name = "Nicht vorhanden"
    suchparameter = HochschuleSuchparameter(name=name)
    pageable = Pageable(size=5, number=0)
    # session.scalars(select(Hochschule)...).all()
    session_mock.scalars.return_value.all.return_value = []

    # Act
    with pytest.raises(NotFoundError) as err:
        hochschule_service.find(suchparameter=suchparameter, pageable=pageable)

    # Assert
    assert err.type == NotFoundError
    assert str(err.value) == "Not Found"
    assert err.value.suchparameter is not None
    assert err.value.suchparameter.name == name  # pyright: ignore[reportOptionalMemberAccess]
