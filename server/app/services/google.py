from typing import Dict, Any
from test import Action, Reaction, Service


class Google(Service):
    class new_email(Action):
        def __init__(self) -> None:
            config = [
                {"name": "from", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
            ]
            super().__init__("Déclenché lorsqu'un nouvel email arrive.", config)

        def check(self, params: Dict[str, Any] = None):
            if params:
                print(
                    f"Checking for new email from: {params.get('from', 'anyone')}, subject: {params.get('subject', 'any')}"
                )
            else:
                print("Checking for new emails in Gmail!")

    class send_email(Reaction):
        def __init__(self) -> None:
            config = [
                {"name": "to", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
                {"name": "body", "type": "input", "values": []},
            ]
            super().__init__("Permet d'envoyer un email.", config)

        def execute(self, params: Dict[str, Any] = None):
            if params:
                print(f"Sending email to: {params.get('to')}")
                print(f"Subject: {params.get('subject')}")
                print(f"Body: {params.get('body')}")
            else:
                print("Sending an email via Gmail!")

    def __init__(self) -> None:
        super().__init__("Service email de Google")
