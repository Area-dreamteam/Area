"""GitHub OAuth integration service.

Provides OAuth login functionality for GitHub accounts.
Allows users to authenticate using their GitHub credentials.

Also provides GitHub automation service for repository and issue management.
"""

from typing import Dict, Any, List
from services.oauth_lib import oauth_add_login, oauth_add_link
import requests
from urllib.parse import urlencode
from models.users.user import User
from models.users.user_service import UserService
from models.services.service import Service
from sqlmodel import select
from fastapi import HTTPException, Response, Request
from core.config import settings
from core.categories import ServiceCategory

from pydantic import BaseModel
from services.services_classes import (
    oauth_service,
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from sqlmodel import Session
from pydantic_core import ValidationError
from core.utils import generate_state
from core.logger import logger
from api.users.db import get_user_service_token


class GithubOAuthTokenRes(BaseModel):
    """GitHub OAuth token response format."""

    access_token: str
    token_type: str
    scope: str


class GithubApiError(Exception):
    """GitHub API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GithubOauth(oauth_service):
    """GitHub OAuth service for user authentication."""

    def __init__(self) -> None:
        super().__init__(color="#000000", img_url="/images/Github_logo.webp")

    def _get_token(self, client_id, client_secret, code):
        """Exchange authorization code for access token."""
        base_url = "https://github.com/login/oauth/access_token"
        params = {"client_id": client_id, "client_secret": client_secret, "code": code}

        r = requests.post(
            f"{base_url}?{urlencode(params)}", headers={"Accept": "application/json"}
        )

        if r.status_code != 200:
            raise GithubApiError("Invalid code or failed to retrieve token")

        try:
            return GithubOAuthTokenRes(**r.json())
        except ValidationError:
            raise GithubApiError("Invalid OAuth response")

    def _get_email(self, token):
        """Fetch user email from GitHub API."""
        base_url = "https://api.github.com/user/emails"
        email_r = requests.get(
            f"{base_url}",
            headers={"Authorization": f"token {token}", "Accept": "application/json"},
        )

        if email_r.status_code != 200:
            raise GithubApiError("Failed to retrieve mail")

        return email_r.json()

    def oauth_link(self, state: str = "") -> str:
        """Generate GitHub OAuth authorization URL."""
        base_url = "https://github.com/login/oauth/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/login/{self.name}"
        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": redirect,
            "prompt": "select_account",
            "allow_signup": "true",
            "scope": "read:user user:email",
            "login": "",
            "force_verify": "true",
        }
        if state:
            params["state"] = state
        else:
            params["state"] = generate_state()
        return f"{base_url}?{urlencode(params)}"

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request | None = None,
        is_mobile: bool = False,
    ) -> Response:
        """Handle GitHub OAuth callback and create/authenticate user."""
        try:
            token_res = self._get_token(
                settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET, code
            )
        except GithubApiError as e:
            raise HTTPException(status_code=400, detail=e.message)
        try:
            user_info = self._get_email(token_res.access_token)[0]
        except GithubApiError as e:
            raise HTTPException(status_code=400, detail=e.message)
        return oauth_add_login(
            session,
            self.name,
            user,
            token_res.access_token,
            user_info["email"],
            request,
            is_mobile,
        )


class Github(ServiceClass):
    """GitHub automation service for repository and issue management."""

    def __init__(self) -> None:
        super().__init__(
            "GitHub Repository and Issue Management",
            ServiceCategory.DEVELOPER,
            "#000000",
            "images/Github_logo.webp",
            True,
        )

    class new_repository(Action):
        """Triggered when a new repository is created by the authenticated user."""

        service: "Github"

        def __init__(self):
            super().__init__(
                "Triggered when a new repository is created by the authenticated user",
                [],
            )

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)

            try:
                repositories = self.service._get_user_repositories(token)
            except GithubApiError as e:
                logger.error(f"GitHub new_repository check error: {e.message}")
                return False

            repo_ids = {repo["id"] for repo in repositories}
            previous_repo_ids = set(
                area_action.last_state.get("repo_ids", [])
                if area_action.last_state
                else []
            )

            if not area_action.last_state or "repo_ids" not in area_action.last_state:
                area_action.last_state = {"repo_ids": list(repo_ids)}
                session.add(area_action)
                session.commit()
                return False

            area_action.last_state = {"repo_ids": list(repo_ids)}
            session.add(area_action)
            session.commit()

            new_repos = repo_ids - previous_repo_ids
            return len(new_repos) > 0

    class new_issue(Action):
        """Triggered when a new issue is created in a watched repository."""

        service: "Github"

        def __init__(self):
            config_schema = [
                {"name": "Repository Owner", "type": "input", "values": []},
                {"name": "Repository Name", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a new issue is created in a watched repository",
                config_schema,
            )

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            owner = get_component(area_action.config, "Repository Owner", "values")
            repo = get_component(area_action.config, "Repository Name", "values")

            try:
                issues = self.service._get_repository_issues(token, owner, repo)
            except GithubApiError as e:
                logger.error(f"GitHub new_issue check error: {e.message}")
                return False

            issue_ids = {issue["id"] for issue in issues}
            previous_issue_ids = set(
                area_action.last_state.get("issue_ids", [])
                if area_action.last_state
                else []
            )

            if not area_action.last_state or "issue_ids" not in area_action.last_state:
                area_action.last_state = {"issue_ids": list(issue_ids)}
                session.add(area_action)
                session.commit()
                return False

            area_action.last_state = {"issue_ids": list(issue_ids)}
            session.add(area_action)
            session.commit()

            new_issues = issue_ids - previous_issue_ids
            return len(new_issues) > 0

    class new_pull_request(Action):
        """Triggered when a new pull request is created in a watched repository."""

        service: "Github"

        def __init__(self):
            config_schema = [
                {"name": "Repository Owner", "type": "input", "values": []},
                {"name": "Repository Name", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a new pull request is created in a watched repository",
                config_schema,
            )

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            owner = get_component(area_action.config, "Repository Owner", "values")
            repo = get_component(area_action.config, "Repository Name", "values")

            try:
                pulls = self.service._get_repository_pulls(token, owner, repo)
            except GithubApiError as e:
                logger.error(f"GitHub new_pull_request check error: {e.message}")
                return False

            pr_ids = {pr["id"] for pr in pulls}
            previous_pr_ids = set(
                area_action.last_state.get("pr_ids", [])
                if area_action.last_state
                else []
            )

            if not area_action.last_state or "pr_ids" not in area_action.last_state:
                area_action.last_state = {"pr_ids": list(pr_ids)}
                session.add(area_action)
                session.commit()
                return False

            area_action.last_state = {"pr_ids": list(pr_ids)}
            session.add(area_action)
            session.commit()

            new_prs = pr_ids - previous_pr_ids
            return len(new_prs) > 0

    class repo_star_threshold(Action):
        """Triggered when a repository reaches a star count threshold."""

        service: "Github"

        def __init__(self):
            config_schema = [
                {"name": "Repository Owner", "type": "input", "values": []},
                {"name": "Repository Name", "type": "input", "values": []},
                {"name": "Star Threshold", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a repository reaches a star count threshold",
                config_schema,
            )

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            owner = get_component(area_action.config, "Repository Owner", "values")
            repo = get_component(area_action.config, "Repository Name", "values")
            threshold_str = get_component(
                area_action.config, "Star Threshold", "values"
            )

            try:
                threshold = int(threshold_str)
            except (ValueError, TypeError):
                logger.error(f"Invalid star threshold: {threshold_str}")
                return False

            try:
                repo_data = self.service._get_repository(token, owner, repo)
            except GithubApiError as e:
                logger.error(f"GitHub repo_star_threshold check error: {e.message}")
                return False

            current_stars = repo_data.get("stargazers_count", 0)
            previous_triggered = (
                area_action.last_state.get("triggered", False)
                if area_action.last_state
                else False
            )

            if current_stars >= threshold and not previous_triggered:
                area_action.last_state = {"triggered": True}
                session.add(area_action)
                session.commit()
                return True

            area_action.last_state = {"triggered": previous_triggered}
            session.add(area_action)
            session.commit()
            return False

    class create_issue(Reaction):
        """Create a new issue in a specified repository."""

        service: "Github"

        def __init__(self):
            config_schema = [
                {"name": "Repository Owner", "type": "input", "values": []},
                {"name": "Repository Name", "type": "input", "values": []},
                {"name": "Issue Title", "type": "input", "values": []},
                {"name": "Issue Body", "type": "input", "values": []},
            ]
            super().__init__(
                "Create a new issue in a specified repository", config_schema
            )

        def execute(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            owner = get_component(area_action.config, "Repository Owner", "values")
            repo = get_component(area_action.config, "Repository Name", "values")
            title = get_component(area_action.config, "Issue Title", "values")
            body = get_component(area_action.config, "Issue Body", "values")

            try:
                self.service._create_issue(token, owner, repo, title, body)
                logger.info(f"{self.service.name} - {self.name} - Created issue '{title}' in {owner}/{repo} - User: {user_id}")
            except GithubApiError as e:
                logger.error(f"Failed to create issue: {e.message}")

    class star_repository(Reaction):
        """Star a repository on GitHub."""

        service: "Github"

        def __init__(self):
            config_schema = [
                {"name": "Repository Owner", "type": "input", "values": []},
                {"name": "Repository Name", "type": "input", "values": []},
            ]
            super().__init__("Star a repository on GitHub", config_schema)

        def execute(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            owner = get_component(area_action.config, "Repository Owner", "values")
            repo = get_component(area_action.config, "Repository Name", "values")

            try:
                self.service._star_repository(token, owner, repo)
                logger.info(f"{self.service.name} - {self.name} - Starred repository {owner}/{repo} - User: {user_id}")
            except GithubApiError as e:
                logger.error(f"Failed to star repository: {e.message}")

    class comment_on_pr(Reaction):
        """Add a comment to a pull request."""

        service: "Github"

        def __init__(self):
            config_schema = [
                {"name": "Repository Owner", "type": "input", "values": []},
                {"name": "Repository Name", "type": "input", "values": []},
                {"name": "PR Number", "type": "input", "values": []},
                {"name": "Comment Body", "type": "input", "values": []},
            ]
            super().__init__("Add a comment to a pull request", config_schema)

        def execute(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            owner = get_component(area_action.config, "Repository Owner", "values")
            repo = get_component(area_action.config, "Repository Name", "values")
            pr_number_str = get_component(area_action.config, "PR Number", "values")
            comment = get_component(area_action.config, "Comment Body", "values")

            try:
                pr_number = int(pr_number_str)
            except (ValueError, TypeError):
                logger.error(f"Invalid PR number: {pr_number_str}")
                return

            try:
                self.service._comment_on_pull_request(
                    token, owner, repo, pr_number, comment
                )
                logger.info(f"{self.service.name} - {self.name} - Commented on PR #{pr_number} in {owner}/{repo} - User: {user_id}")
            except GithubApiError as e:
                logger.error(f"Failed to comment on PR: {e.message}")

    def _get_token(
        self, client_id: str, client_secret: str, code: str
    ) -> GithubOAuthTokenRes:
        """Exchange authorization code for access token."""
        base_url = "https://github.com/login/oauth/access_token"
        params = {"client_id": client_id, "client_secret": client_secret, "code": code}

        r = requests.post(
            f"{base_url}?{urlencode(params)}", headers={"Accept": "application/json"}
        )

        if r.status_code != 200:
            raise GithubApiError("Invalid code or failed to retrieve token")

        try:
            return GithubOAuthTokenRes(**r.json())
        except ValidationError:
            raise GithubApiError("Invalid OAuth response")

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        """Fetch authenticated user information from GitHub API."""
        url = "https://api.github.com/user"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            raise GithubApiError(f"Failed to retrieve user info: {r.text}")

        return r.json()

    def _is_token_valid(self, token: str) -> bool:
        """Check if GitHub access token is valid."""
        try:
            self._get_user_info(token)
            return True
        except GithubApiError:
            return False

    def _make_github_request(
        self,
        token: str,
        endpoint: str,
        method: str = "GET",
        data: Dict[str, Any] | None = None,
        return_list: bool = False,
    ) -> Dict[str, Any] | List[Dict[str, Any]]:
        """Make authenticated GitHub API request."""
        url = f"https://api.github.com{endpoint}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if method == "GET":
            r = requests.get(url, headers=headers)
        elif method == "POST":
            r = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            r = requests.put(url, headers=headers, json=data)
        else:
            raise GithubApiError(f"Unsupported HTTP method: {method}")

        if r.status_code not in [200, 201, 204]:
            raise GithubApiError(f"GitHub API error: {r.status_code} - {r.text}")

        if not r.text:
            return [] if return_list else {}

        result = r.json()
        return result if return_list or isinstance(result, list) else result

    def _get_user_repositories(self, token: str) -> List[Dict[str, Any]]:
        """Fetch all repositories for the authenticated user."""
        result = self._make_github_request(
            token, "/user/repos?sort=created&per_page=100", return_list=True
        )
        return result if isinstance(result, list) else []

    def _get_repository_issues(
        self, token: str, owner: str, repo: str
    ) -> List[Dict[str, Any]]:
        """Fetch issues for a specific repository."""
        result = self._make_github_request(
            token,
            f"/repos/{owner}/{repo}/issues?state=all&per_page=100",
            return_list=True,
        )
        return result if isinstance(result, list) else []

    def _get_repository_pulls(
        self, token: str, owner: str, repo: str
    ) -> List[Dict[str, Any]]:
        """Fetch pull requests for a specific repository."""
        result = self._make_github_request(
            token,
            f"/repos/{owner}/{repo}/pulls?state=all&per_page=100",
            return_list=True,
        )
        return result if isinstance(result, list) else []

    def _get_repository(self, token: str, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch details for a specific repository."""
        result = self._make_github_request(token, f"/repos/{owner}/{repo}")
        return result if isinstance(result, dict) else {}

    def _create_issue(
        self, token: str, owner: str, repo: str, title: str, body: str = ""
    ) -> Dict[str, Any]:
        """Create a new issue in a repository."""
        data = {"title": title, "body": body}
        result = self._make_github_request(
            token, f"/repos/{owner}/{repo}/issues", method="POST", data=data
        )
        return result if isinstance(result, dict) else {}

    def _star_repository(self, token: str, owner: str, repo: str) -> Dict[str, Any]:
        """Star a repository."""
        result = self._make_github_request(
            token, f"/user/starred/{owner}/{repo}", method="PUT"
        )
        return result if isinstance(result, dict) else {}

    def _comment_on_pull_request(
        self, token: str, owner: str, repo: str, pr_number: int, body: str
    ) -> Dict[str, Any]:
        """Add a comment to a pull request."""
        data = {"body": body}
        result = self._make_github_request(
            token,
            f"/repos/{owner}/{repo}/issues/{pr_number}/comments",
            method="POST",
            data=data,
        )
        return result if isinstance(result, dict) else {}

    def is_connected(self, session: Session, user_id: int) -> bool:
        """Check if user has connected their GitHub account."""
        user_service = session.exec(
            select(UserService)
            .join(Service)
            .where(
                UserService.user_id == user_id,
                Service.name == self.name,
            )
        ).first()
        if not user_service:
            return False

        return self._is_token_valid(user_service.access_token)

    def oauth_link(self, state: str = "") -> str:
        """Generate GitHub OAuth authorization URL for service linking."""
        base_url = "https://github.com/login/oauth/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.GITHUB_LINK_CLIENT_ID,
            "redirect_uri": redirect,
            "scope": "repo read:user read:org",
            "state": state if state else generate_state(),
        }
        return f"{base_url}?{urlencode(params)}"

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request | None = None,
        is_mobile: bool = False,
    ) -> Response:
        """Handle GitHub OAuth callback for service linking."""
        try:
            token_res = self._get_token(
                settings.GITHUB_LINK_CLIENT_ID,
                settings.GITHUB_LINK_CLIENT_SECRET,
                code,
            )
        except GithubApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(
            session, self.name, user, token_res.access_token, request, is_mobile
        )
