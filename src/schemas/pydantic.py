from datetime import timedelta
from pydantic import BaseModel

# --- Pydantic models ---
class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


class TokenResponse(BaseModel):
    token: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: timedelta


class TestUserLogin(BaseModel):
    username: str = "testuser"
    password: str = "testpassword"  # Default password for testuser