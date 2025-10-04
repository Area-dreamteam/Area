from pydantic import BaseModel
from pydantic_core import ValidationError
from urllib.parse import urlencode
import requests



class GithubOAuthTokenRes(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int


class GithubApiError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GithubApi:
    def __init__(self):
        pass
    
    def get_oauth_link(self, client_id, redirect):
        base_url = "https://github.com/login/oauth/authorize"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect
        }
        return f"{base_url}?{urlencode(params)}"
    
    def get_token(self, client_id, client_secret, code):
        base_url = "https://github.com/login/oauth/access_token"
        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code
        }
        
        r = requests.post(f"{base_url}?{urlencode(params)}", headers={"Accept": "application/json"})
        
        if r.status_code != 200:
            raise GithubApiError("Invalid code or failed to retrieve token")
        
        try:
            return GithubOAuthTokenRes(**r.json())
        except ValidationError:
            raise GithubApiError("Invalid OAuth response")
    
    def get_email(self, token):
        base_url = "https://api.github.com/user/emails"
        email_r = requests.get(f"{base_url}", headers={"Authorization": f"token {token}", "Accept": "application/json"})
        
        if email_r.status_code != 200:
            raise GithubApiError("Failed to retrieve mail")

        return email_r.json()


github_api = GithubApi()
