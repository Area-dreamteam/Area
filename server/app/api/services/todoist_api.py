from pydantic import BaseModel
from pydantic_core import ValidationError
from urllib.parse import urlencode
import requests
import json

from core.utils import generate_state



class TodoistOAuthTokenRes(BaseModel):
    access_token: str
    token_type: str


class TodoistApiError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TodoistApi:
    def __init__(self):
        pass
    
    def get_oauth_link(self, client_id, redirect):
        base_url = "https://todoist.com/oauth/authorize"
        params = {
            "client_id": client_id,
            "scope": "data:read,data:delete",
            "state": generate_state()
        }
        return f"{base_url}?{urlencode(params)}"
    
    def get_token(self, client_id, client_secret, code):
        base_url = "https://todoist.com/oauth/access_token"
        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code
        }
        
        r = requests.post(f"{base_url}?{urlencode(params)}", headers={"Accept": "application/json"})
        
        if r.status_code != 200:
            raise TodoistApiError("Invalid code or failed to retrieve token")
        
        try:
            return TodoistOAuthTokenRes(**r.json())
        except ValidationError:
            raise TodoistApiError("Invalid OAuth response")
    
    def get_user_info(self, token):
        base_url = "https://api.todoist.com/api/v1/sync"
        params = {
            "sync_token": "\'*\'",
            "resource_types": json.dumps(["user"])
        }
        email_r = requests.post(f"{base_url}?{urlencode(params)}", headers={"Authorization": f"Bearer {token}"})
        
        if email_r.status_code != 200:
            raise TodoistApiError("Failed to retrieve todo")

        return email_r.json()["user"]


todoist_api = TodoistApi()
