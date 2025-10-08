from reactions.create_task import get_component
from core.logger import logger
from typing import Any
from dependencies.db import SessionDep
import smtplib
from email.message import EmailMessage


def send_email(subject, body, to_email, from_email, password):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    # For HTML emails
    # msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def gmail_reaction(session: SessionDep, user_id: int, config: list) -> None:
    send_email(
        subject=get_component(config, "subject", "values"),
        body=get_component(config, "body", "values"),
        to_email=get_component(config, "to", "values"),
        from_email="area.area.noreply@gmail.com",
        password="zijc yqel ojxi eidb",
    )
