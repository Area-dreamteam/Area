# Creating New Services Guide

## Overview

The AREA platform uses a modular service architecture that automatically discovers and registers new services. This guide shows how to create new service integrations with actions, reactions, and OAuth support.

## Service Architecture

### Base Classes

- **`Service`**: Full automation service with actions and reactions
- **`oauth_service`**: OAuth-only service for authentication without automation
- **`Action`**: Automation triggers (periodic checks)
- **`Reaction`**: Automation responses (executed when actions trigger)

### Auto-Discovery

Services are automatically discovered and registered using Python's class inheritance system. Simply create a subclass and it will be included in the service catalog.

## Creating a Basic Service

### 1. Basic Service Structure

```python
# services/my_service.py
from services.services_classes import Service, Action, Reaction
from sqlmodel import Session
from models import AreaAction, AreaReaction

class MyService(Service):
    """My custom automation service."""
    
    def __init__(self) -> None:
        super().__init__(
            description="Description of your service",
            category="Category (e.g., 'Social', 'Productivity')",
            color="#ff6b6b",  # UI theme color
            img_url="https://example.com/logo.png",
            oauth=True  # Set to False if no OAuth needed
        )
```

### 2. Adding Actions (Triggers)

Actions are nested classes that inherit from `Action`:

```python
class MyService(Service):
    class new_message(Action):
        """Trigger when new message is received."""
        def __init__(self) -> None:
            config_schema = [
                {"name": "channel", "type": "input", "values": []},
                {"name": "keyword", "type": "input", "values": []}
            ]
            super().__init__(
                "Triggers when new message contains keyword",
                config_schema,
                interval="*/5 * * * *"  # Every 5 minutes
            )
        
        def check(self, session: Session, area_action: AreaAction, user_id: int) -> bool:
            # Implement your trigger logic here
            # Return True if condition is met
            config = area_action.config
            channel = config.get("channel")
            keyword = config.get("keyword")
            
            # Your API calls and logic here
            return self._check_for_messages(channel, keyword, user_id)
        
        def _check_for_messages(self, channel: str, keyword: str, user_id: int) -> bool:
            # Helper method for cleaner code
            pass
```

### 3. Adding Reactions (Responses)

Reactions are also nested classes:

```python
class MyService(Service):
    class send_message(Reaction):
        """Send message to channel."""
        def __init__(self) -> None:
            config_schema = [
                {"name": "channel", "type": "input", "values": []},
                {"name": "message", "type": "textarea", "values": []},
                {
                    "name": "priority", 
                    "type": "select", 
                    "values": ["low", "normal", "high"]
                }
            ]
            super().__init__(
                "Send message to specified channel",
                config_schema
            )
        
        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            # Implement your reaction logic here
            config = area_reaction.config
            channel = config.get("channel")
            message = config.get("message")
            priority = config.get("priority")
            
            # Your API calls here
            self._send_message(channel, message, priority, user_id)
        
        def _send_message(self, channel: str, message: str, priority: str, user_id: int):
            # Helper method for API calls
            pass
```

## Configuration Schema Types

Configuration schemas define the UI forms for user customization:

```python
config_schema = [
    # Text input
    {"name": "field_name", "type": "input", "values": []},
    
    # Textarea
    {"name": "description", "type": "textarea", "values": []},
    
    # Dropdown selection
    {"name": "priority", "type": "select", "values": ["low", "high", "urgent"]},
    
    # Multiple checkboxes
    {
        "name": "notifications", 
        "type": "check_list", 
        "values": {"email": True, "sms": False, "push": True}
    }
]
```

## OAuth Integration

### 1. OAuth Configuration

For services requiring OAuth authentication:

```python
class MyService(Service):
    def __init__(self) -> None:
        super().__init__(
            # ... other params
            oauth=True
        )
    
    def oauth_link(self) -> str:
        """Generate OAuth authorization URL."""
        from urllib.parse import urlencode
        from core.config import settings
        
        base_url = "https://myservice.com/oauth/authorize"
        params = {
            "client_id": settings.MYSERVICE_CLIENT_ID,
            "redirect_uri": f"{settings.FRONT_URL}/callbacks/myservice",
            "scope": "read write",
            "response_type": "code"
        }
        return f"{base_url}?{urlencode(params)}"
    
    def oauth_callback(self, session: Session, code: str, user: User) -> Response:
        """Handle OAuth callback."""
        from services.oauth_lib import oauth_add_link
        
        try:
            token_response = self._exchange_code_for_token(code)
        except MyServiceApiError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        return oauth_add_link(
            session, 
            self.name, 
            user, 
            token_response.access_token
        )
```

### 2. Token Management

Helper methods for OAuth token handling:

```python
class MyServiceOAuthTokenRes(BaseModel):
    """OAuth token response format."""
    access_token: str
    token_type: str
    expires_in: int

class MyServiceApiError(Exception):
    """Service-specific API errors."""
    pass

def _exchange_code_for_token(self, code: str) -> MyServiceOAuthTokenRes:
    """Exchange authorization code for access token."""
    import requests
    from urllib.parse import urlencode
    from core.config import settings
    
    url = "https://myservice.com/oauth/token"
    data = {
        "client_id": settings.MYSERVICE_CLIENT_ID,
        "client_secret": settings.MYSERVICE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code != 200:
        raise MyServiceApiError("Failed to get access token")
    
    return MyServiceOAuthTokenRes(**response.json())
```

## OAuth-Only Services

For services that only provide authentication without automation:

```python
# services/my_oauth_service.py
from services.services_classes import oauth_service
from services.oauth_lib import oauth_add_login

class my_oauth_service(oauth_service):
    """OAuth login service without automation."""
    
    def __init__(self) -> None:
        super().__init__(
            color="#4285f4",
            img_url="https://example.com/logo.png"
        )
    
    def oauth_link(self) -> str:
        # Same as full service OAuth
        pass
    
    def oauth_callback(self, session: Session, code: str, user: User | None) -> Response:
        """Handle OAuth login flow."""
        try:
            token_response = self._exchange_code_for_token(code)
            user_info = self._get_user_info(token_response.access_token)
        except MyServiceApiError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        return oauth_add_login(
            session,
            self.name,
            user,
            token_response.access_token,
            user_info["email"]
        )
```

## Best Practices

### 1. Error Handling

```python
class MyServiceApiError(Exception):
    """Service-specific API errors with clear messages."""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def _api_request(self, endpoint: str, token: str) -> dict:
    """Make authenticated API request with error handling."""
    import requests
    
    try:
        response = requests.get(
            f"https://api.myservice.com{endpoint}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 401:
            raise MyServiceApiError("Invalid or expired token", 401)
        elif response.status_code != 200:
            raise MyServiceApiError(f"API error: {response.status_code}")
        
        return response.json()
        
    except requests.RequestException as e:
        raise MyServiceApiError(f"Network error: {str(e)}")
```

### 2. Token Validation

```python
def _is_token_valid(self, token: str) -> bool:
    """Check if access token is still valid."""
    try:
        self._api_request("/user/profile", token)
        return True
    except MyServiceApiError:
        return False

def is_connected(self, session: Session, user_id: int) -> bool:
    """Check if service is connected for user."""
    from models.users.user_service import UserService
    from models.services.service import Service
    from sqlmodel import select
    
    user_service = session.exec(
        select(UserService)
        .join(Service)
        .where(Service.name == self.name, UserService.user_id == user_id)
    ).first()
    
    if not user_service:
        return False
    
    return self._is_token_valid(user_service.access_token)
```

### 3. Configuration Validation

```python
def _validate_config(self, config: dict, schema: list) -> bool:
    """Validate user configuration against schema."""
    for field in schema:
        field_name = field["name"]
        if field_name not in config:
            raise ValueError(f"Missing required field: {field_name}")
        
        if field["type"] == "select":
            if config[field_name] not in field["values"]:
                raise ValueError(f"Invalid value for {field_name}")
    
    return True
```

## Environment Configuration

Add your service credentials to the environment configuration:

```python
# core/config.py
class Settings(BaseSettings):
    # ... existing settings
    MYSERVICE_CLIENT_ID: str
    MYSERVICE_CLIENT_SECRET: str
    MYSERVICE_API_KEY: str = ""  # Optional fields with defaults
```

## Registration

Services are automatically registered when imported. Add your service import to `services/services.py`:

```python
# services/services.py
from services.my_service import MyService
from services.my_oauth_service import my_oauth_service
# ... other imports
```

## Database Schema

The service data is automatically synced to the database. Your service information will appear in:

- `services` table - Service metadata
- `actions` table - Available actions
- `reactions` table - Available reactions
- `user_services` table - User OAuth connections

## Testing Your Service

1. **Start the server**: The service will be auto-registered
2. **Check API**: Visit `/docs` to see your service in the OpenAPI documentation
3. **Test OAuth**: Use `/oauth/index/{service_name}` to test OAuth flow
4. **Create Areas**: Use the frontend to create automation areas with your service

## Common Patterns

### Polling vs Webhooks

```python
# Polling pattern (most common)
class poll_for_updates(Action):
    def check(self, session: Session, area_action: AreaAction, user_id: int) -> bool:
        # Check API for changes since last check
        last_check = area_action.last_execution or datetime.now()
        updates = self._get_updates_since(last_check, user_id)
        return len(updates) > 0

# Webhook pattern (advanced)
class webhook_trigger(Action):
    def check(self, session: Session, area_action: AreaAction, user_id: int) -> bool:
        # Check if webhook was received (stored in cache/database)
        return self._check_webhook_received(area_action.id)
```

### Batch Operations

```python
class bulk_operation(Reaction):
    def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
        config = area_reaction.config
        items = config.get("items", [])
        
        # Process in batches to avoid API rate limits
        batch_size = 10
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            self._process_batch(batch, user_id)
            time.sleep(1)  # Rate limiting
```

This guide covers the essential patterns for creating new services. The modular architecture makes it easy to add new integrations while maintaining consistency and automatic discovery.