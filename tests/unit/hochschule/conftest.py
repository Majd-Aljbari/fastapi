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

"""Fixture für pytest: Repository, Hochschule(Write)Service."""

import pytest

from hochschule.repository import HochschuleRepository
from hochschule.service import HochschuleService, HochschuleWriteService


@pytest.fixture
def hochschule_repository() -> HochschuleRepository:
    """Fixture für HochschuleRepository."""
    return HochschuleRepository()


@pytest.fixture
def hochschule_service(
    hochschule_repository: HochschuleRepository,
) -> HochschuleService:
    """Fixture für HochschuleService."""
    return HochschuleService(hochschule_repository)


@pytest.fixture
def hochschule_write_service(
    hochschule_repository: HochschuleRepository,
) -> HochschuleWriteService:
    """Fixture für HochschuleWriteService."""
    return HochschuleWriteService(hochschule_repository)
