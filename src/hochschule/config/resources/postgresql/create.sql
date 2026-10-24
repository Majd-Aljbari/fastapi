-- Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.

-- https://www.postgresql.org/docs/current/manage-ag-tablespaces.html
SET default_tablespace = hochschulespace;

-- https://www.postgresql.org/docs/current/sql-createtable.html
CREATE TABLE IF NOT EXISTS hochschule (
    id           INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    version      INTEGER NOT NULL DEFAULT 0,
    name         TEXT NOT NULL UNIQUE,
    homepage     TEXT,
    erzeugt      TIMESTAMP NOT NULL,
    aktualisiert TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS hochschule_name_idx ON hochschule(name);

CREATE TABLE IF NOT EXISTS adresse (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    strasse         TEXT NOT NULL,
    hausnummer      TEXT NOT NULL,
    plz             TEXT NOT NULL CHECK (plz ~ '\d{5}'),
    ort             TEXT NOT NULL,
    hochschule_id   INTEGER NOT NULL UNIQUE REFERENCES hochschule ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS adresse_hochschule_id_idx ON adresse(hochschule_id);

CREATE TABLE IF NOT EXISTS student (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    matrikelnummer  TEXT NOT NULL,
    vorname         TEXT NOT NULL,
    nachname        TEXT NOT NULL,
    email           TEXT NOT NULL,
    hochschule_id   INTEGER NOT NULL REFERENCES hochschule ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS student_hochschule_id_idx ON student(hochschule_id);
