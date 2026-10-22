"""Funktionen für E-Mails."""

from email.message import EmailMessage
from email.utils import make_msgid
from smtplib import SMTP, SMTPServerDisconnected
from socket import gaierror
from typing import Final
from uuid import uuid4

from loguru import logger

from hochschule.config import mail_config, receiver, sender
from hochschule.service.hochschule_dto import HochschuleDTO

__all__ = ["send_mail"]


def send_mail(hochschule_dto: HochschuleDTO) -> None:
    """Funktion, um eine E-Mail beim Anlegen einer neuen Hochschule zu senden.

    :param hochschule_dto: Hochschuldaten
    """
    logger.debug("{}", hochschule_dto)
    if not mail_config.enabled:
        logger.warning("send_mail: Der Mailserver ist deaktiviert")
        return

    msg: Final = EmailMessage()
    msg["From"] = sender
    msg["To"] = (receiver,)
    msg["Subject"] = f"Neue Hochschule angelegt: ID={hochschule_dto.id}"
    msg["Message-ID"] = make_msgid(idstring=str(uuid4()))

    msg.set_content(f"Neue Hochschule: {hochschule_dto.name}")

    asparagus_cid: Final = make_msgid()
    msg.add_alternative(
        f"Neue Hochschule: <b>{hochschule_dto.name}</b>".format(
            asparagus_cid=asparagus_cid[1:-1]
        ),
        subtype="html",
    )

    try:
        with SMTP(
            host=mail_config.host, port=mail_config.port, timeout=mail_config.timeout
        ) as smtp:
            logger.debug("msg={}", msg)
            smtp.send_message(msg)
    except ConnectionRefusedError:
        logger.warning("ConnectionRefusedError beim Mailserver")
    except SMTPServerDisconnected:
        logger.warning("SMTPServerDisconnected")
    except TimeoutError:
        logger.warning("TimeoutError beim Senden der E-Mail")
    except gaierror:
        logger.warning("socket.gaierror: Läuft der Mailserver im virtuellen Netzwerk?")
