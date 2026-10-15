# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe
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
"""Modul für die REST-Schnittstelle einschließlich Validierung."""

lazy from collections.abc import Sequence

from hochschule.router.health_router import liveness, readiness, router as health_router
from hochschule.router.hello_router import router as hello_router
# TODO: patient_router und patient_write_router durch hochschule_router ersetzen
# from hochschule.router.patient_router import get, get_by_id, get_nachnamen, patient_router, query
# from hochschule.router.patient_write_router import delete_by_id, patient_write_router, post, put
from hochschule.router.shutdown_router import router as shutdown_router, shutdown

__all__: Sequence[str] = [
    "health_router",
    "hello_router",
    "liveness",
    "readiness",
    "shutdown",
    "shutdown_router",
    # "patient_router",
    # "patient_write_router",
]
