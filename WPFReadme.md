# Dokumentation: Einrichtung und Nutzung von Cursor für Python/FastAPI

**Wahlpflichtfach 
**Projekt:** FastAPI Backend (`patient`)  
**Name:** Majd Aldenn Aljbari  
**Matrikelnummer:** 97282

---

## Inhaltsverzeichnis
1. [Einleitung](#1-einleitung)
2. [Installation](#2-installation)
3. [Extensions](#3-extensions)
4. [Projekt einrichten](#4-projekt-einrichten)
5. [Cursor AI-Features](#5-cursor-ai-features)
6. [Konkrete Anwendungsbeispiele am Projekt](#6-konkrete-anwendungsbeispiele-am-projekt)
7. [Vergleich VS Code vs. Cursor](#7-vergleich-vs-code-vs-cursor)

---

## 1. Einleitung

### Was ist Cursor und worin liegt der Unterschied zu VS Code?
Cursor ist eine moderne, KI-zentrierte Entwicklungsumgebung (IDE), die als direkter **Fork von Visual Studio Code** entwickelt wurde. Das bedeutet, dass die grundlegende Benutzeroberfläche, Tastenkombinationen, Einstellungen und das gesamte Extension-Ökosystem identisch mit VS Code sind. 

Der wesentliche Unterschied liegt in der tiefen, nativen Integration von künstlicher Intelligenz. Während bei VS Code KI-Funktionen (wie GitHub Copilot) als nachträgliches Plugin installiert werden müssen, greift Cursor nativ auf den gesamten Projektkontext zu und ermöglicht mehrdateilige Refactorings, intelligentes Code-Completion und kontextbezogene Fehlerbehebung.

### Warum Cursor für Python / FastAPI?
Bei der Entwicklung von modernen Backend-Anwendungen mit **FastAPI**, **Pydantic** und **SQLAlchemy** entstehen komplexe Abhängigkeiten zwischen Datenmodellen, Routern, Authentifizierungsschichten (z. B. Keycloak) und Datenbanken. 

Cursor bietet durch seine Indizierung der gesamten Codebasis (`@codebase`) erhebliche Vorteile:
* **Kontextverständnis:** Die KI versteht projektspezifische Typen, Schema-Definitionen und Hilfsklassen über mehrere Dateien hinweg.
* **Effizienz:** Das Erstellen neuer FastAPI-Endpunkte (inklusive Request-/Response-Schemas) lässt sich automatisiert und konsistent umsetzen.
* **Schnelles Debugging:** Fehlermeldungen beim Serverstart (z. B. Datenbankverbindungs- oder Keycloak-Authentifizierungsfehler) können direkt im Chat analysiert werden.

---

## 2. Installation

### Cursor herunterladen und installieren (Windows)
1. Die offizielle Website [cursor.com](https://www.cursor.com/) aufrufen.
2. Den Installer für Windows (`Cursor Setup.exe`) herunterladen.
3. Die Ausführungsdatei starten und den Anweisungen des Installationsassistenten folgen.

### Erster Start & Account-Erstellung
1. Nach dem ersten Start von Cursor erscheint ein Onboarding-Fenster.
2. Es muss ein **Cursor-Account** erstellt oder ein bestehender Account (via GitHub/Google) verknüpft werden.
3. **Kostenstruktur:** 
   * **Hobby / Free Plan:** Beinhaltet eine monatliche Anzahl an schnellen KI-Anfragen (GPT-4o / Claude 3.5 Sonnet) sowie unbegrenzte langsame Anfragen.
   * **Pro Plan (kostenpflichtig):** Bietet erweiterte Limits für sehr intensive Nutzung. Für den Rahmen dieses Projekts reicht der kostenlose Plan aus.

### Cursor und VS Code nebeneinander betreiben
Cursor speichert seine Konfigurationen in eigenen Systempfaden (`%APPDATA%\Cursor`), stört somit eine bestehende VS Code-Installation nicht und kann problemlos parallel genutzt werden. Beim ersten Setup bietet Cursor an, alle Einstellungen, Keybindings und Extensions **direkt aus VS Code zu importieren**.

---

## 3. Extensions

### Automatische Übernahme aus VS Code
Durch die Import-Funktion beim Erststart werden alle installierten VS Code Extensions automatisch in Cursor übernommen. Alternativ können diese manuell über den Extension Marketplace (`Ctrl+Shift+X`) installiert werden.

### Empfohlene Extensions für dieses Projekt
Für die Arbeit am FastAPI-Backend (`patient`) werden folgende Erweiterungen empfohlen:

| Extension | Publisher | Zweck / Funktion |
| :--- | :--- | :--- |
| **Python** | Microsoft | Syntax-Highlighting, IntelliSense, Debugging-Unterstützung |
| **Pylance** | Microsoft | Erweiterte statische Typprüfung und Auto-Imports |
| **Ruff** | Astral Software | Extrem schneller Linter und Formatter für Python-Code |
| **Docker** | Microsoft | Verwaltung von Container-Instanzen (PostgreSQL, Keycloak) |
| **GitLens** | GitKraken | Detaillierte Git-Historie und Branch-Verwaltung |
| **Even Better TOML** | tamasfe | Syntax-Highlighting und Validierung für `app.toml` |

---

## 4. Projekt einrichten

### Projekt öffnen
Öffne das Projektverzeichnis über das Menü **File $\rightarrow$ Open Folder...** oder im Terminal:
```powershell
cd C:\Users\majda\vscodeprojekt\fastapi
cursor .

Python-Interpreter konfigurieren (uv-Environment)
Das Projekt nutzt den modernen Paketmanager uv. Das dazugehörige virtuelle Environment liegt im Ordner .venv.

Drücke Ctrl+Shift+P, um die Befehlspalette zu öffnen.

Tippe Python: Select Interpreter ein und wähle den Befehl aus.

Wähle den Pfad der uv-Umgebung aus, z. B.:

.\.venv\Scripts\python.exe

.venv und pyproject.toml erkennen lassen
Cursor erkennt das Vorhandensein von pyproject.toml sowie den Ordner .venv automatisch. Sollte die Auto-Complete-Funktion externe Pakete (wie fastapi, sqlalchemy oder python-keycloak) nicht auflösen, kann die Indizierung mit Ctrl+Shift+P -> Developer: Reload Window neu gestartet werden.

---

## 5. Cursor AI Features 
Tab-Completion (Cursor Tab)
Funktion: Geht weit über herkömmliche Autovervollständigung oder GitHub Copilot hinaus.

Besonderheit: Cursor Tab prognostiziert nicht nur das nächste Wort, sondern schlägt ganze Zeilenblöcke vor und berücksichtigt dabei kürzliche Code-Änderungen an anderen Stellen des Projekts.

Chat (Ctrl+L)
Funktion: Öffnet das KI-Chatfenster auf der rechten Seite.

Anwendung: Ermöglicht Fragen zum Code, Erklärungen von Algorithmen oder die Analyse von Fehlermeldungen, ohne den Editor zu verlassen.

Composer (Ctrl+I)
Funktion: Das mächtigste Feature von Cursor zur mehrdateiligen Code-Generierung.

Anwendung: Über ein Prompt-Fenster können Anweisungen gegeben werden, die gleichzeitig Änderungen an mehreren Dateien durchführen (z. B. Erstellen eines neuen Models, Hinzufügen der Repository-Methoden und Anlegen des passenden Routers).

@-Referenzen
Über das @-Symbol im Chat oder Composer kann der Kontext präzise gesteuert werden:

@file: Bindet gezielt eine bestimmte Datei in den Prompt ein (z. B. @app.toml).

@docs: Greift auf Dokumentationen bekannter Bibliotheken (wie FastAPI, SQLAlchemy) zu.

@codebase: Indiziert das gesamte Projekt und durchsucht alle Dateien nach relevantem Kontext.

@folders: Beschränkt den Kontext auf ein spezifisches Modul/Verzeichnis.

## 6. Konkrete Anwendungsbeispiele am Projekt
Beispiel 1: Neue Route in FastAPI mit dem Composer erstellen
Vorgehen: Ctrl+I drücken und folgenden Prompt eingeben:

"Erstelle einen neuen GET-Endpunkt /patienten/{id}/historie im Router patient_router.py. Nutze Pydantic für die Response-Validierung und binde die Service-Schicht ein."

Ergebnis: Der Composer schlägt die Änderungen im Router sowie Anpassungen im Schema-Modul vor.

Beispiel 2: Fehler debuggen mit dem Chat
Vorgehen: Fehlermeldung im Terminal markieren (z. B. psycopg.OperationalError: connection failed: SSL error oder KeycloakAuthenticationError: 401) und Ctrl+L drücken.

Prompt:

"Analysiere diesen Traceback. Welche Einstellungen in @app.toml oder @db.py müssen angepasst werden, um das Problem zu beheben?"

Ergebnis: Die KI analysiert den Fehler im Kontext der Konfigurationsdatei und schlägt konkrete Korrekturen vor.

Beispiel 3: Unit-Tests generieren lassen
Vorgehen: Eine bestehende Service-Datei öffnen, den relevanten Code markieren und im Chat (Ctrl+L) auffordern:

"Schreibe passende pytest-Testfälle für diese Methode unter Verwendung von Mocks für die Datenbankverbindung."