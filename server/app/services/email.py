from email.message import EmailMessage
from sqlmodel import Session
from core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from models import AreaReaction
from services.services_classes import Service, Reaction, get_component
from core.categories import ServiceCategory
from core.logger import logger


class EmailError(Exception):
    """Email service specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Email(Service):
    """SMTP Email service.

    Provides simple SMTP email sending functionality.
    Supports any SMTP server with username/password authentication.
    """

    class send_email(Reaction):
        """Send email via SMTP."""

        service: "Email"

        def __init__(self) -> None:
            config_schema = [
                {"name": "to_address", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
                {"name": "body", "type": "input", "values": []},
            ]
            super().__init__("Send email via SMTP", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                smtp_server = "smtp.gmail.com"
                smtp_port = 465
                username = settings.EMAIL
                password = settings.EMAIL_PASSWORD
                from_address = settings.EMAIL
                to_address = get_component(area_action.config, "to_address", "values")
                subject = get_component(area_action.config, "subject", "values")
                body = get_component(area_action.config, "body", "values")

                message = EmailMessage()
                message["From"] = from_address
                message["To"] = to_address
                message["Subject"] = subject
                message.set_content(body)
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(username, password)
                    server.send_message(message)

                logger.debug(f"Email: Successfully sent email to {to_address}")
            except smtplib.SMTPException as e:
                logger.error(f"Email: SMTP error - {str(e)}")
                raise EmailError(f"SMTP error: {str(e)}")
            except Exception as e:
                logger.error(f"Email: Failed to send email - {str(e)}")
                raise EmailError(f"Failed to send email: {str(e)}")

    def __init__(self) -> None:
        super().__init__(
            "Service Email SMTP",
            ServiceCategory.MAIL,
            "#4A90E2",
            "/images/Email_logo.webp",
            False,
        )
