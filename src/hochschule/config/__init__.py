"""Modul zur Konfiguration."""

from hochschule.config.db import (
    db_connect_args,
    db_dialect,
    db_log_statements,
    db_url,
    db_url_admin,
)
from hochschule.config.dev_modus import dev_db_populate, dev_keycloak_populate
from hochschule.config.excel import excel_enabled
from hochschule.config.graphql import graphql_ide
from hochschule.config.keycloak import (
    csv_config,
    keycloak_admin_config,
    keycloak_config,
)
from hochschule.config.mail import mail_config, receiver, sender
from hochschule.config.server import host_binding, port, profiling
from hochschule.config.tls import tls_certfile, tls_keyfile

__all__ = [
    "csv_config",
    "db_connect_args",
    "db_dialect",
    "db_log_statements",
    "db_url",
    "db_url_admin",
    "dev_db_populate",
    "dev_keycloak_populate",
    "excel_enabled",
    "graphql_ide",
    "host_binding",
    "keycloak_admin_config",
    "keycloak_config",
    "mail_config",
    "port",
    "profiling",
    "receiver",
    "sender",
    "tls_certfile",
    "tls_keyfile",
]
