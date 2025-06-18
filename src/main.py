import os
from typing import Any, Optional
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from .schemas.pydantic import ChatRequest, ChatResponse, TestUserLogin, Token
from .ai.gemini import Gemini
from .auth.auth import get_user_id, oauth2_scheme
from .auth.auth import create_jwt_token
from .auth.throttling import apply_rate_limit
from dotenv import load_dotenv
load_dotenv()

# --- FastAPI application instance ---
app = FastAPI()


# --- Load AI Configuration- system prompt and API key ---
def load_system_prompt() -> Optional[str]:
    """
    Load the system prompt from a text file.
    :return: The system prompt as a string.
    """
    system_prompt_path = os.getenv(
        "SYSTEM_PROMPT_PATH", "src/prompts/system_prompt.md")

    # Read the system prompt from the specified file
    try:
        with open(os.path.join(system_prompt_path), 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: System prompt file not found at {system_prompt_path}")
        return None


system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable must be set.")

# Create an instance of the available AI Platform
ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)
# --- FastAPI routes ---


@app.get("/")
async def root():
    return {"message": "Welcome to the Chat API!"}


@app.post("/token")
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Optional[Token]:
    """
    Generate a JWT token for the testuser with default credentials.
    :param form_data: The form_data for the testuser, which should match the default values.
    :raises HTTPException: If the credentials are invalid or if token generation fails.
    :return: A JWT token for the testuser.
    """
    # Generate a JWT token for the testuser
    user_id = form_data.username  # Use the username as the user ID
    user_password = form_data.password  # Use the password as the password
    if user_id == TestUserLogin.model_fields['username'].default and user_password == TestUserLogin.model_fields['password'].default:
        token = await create_jwt_token(user_id)
        print(token)
    elif user_id == TestUserLogin.model_fields['username'].default and user_password != TestUserLogin.model_fields['password'].default:
        raise HTTPException(
            status_code=401,
            detail="Invalid password for testuser."
        )
    else:
        # Implementation for other users can be added here
        token = None
        # raise HTTPException(
        #     status_code=401,
        #     detail=f"Invalid username for testuser. Only 'testuser' with username: {TestUserLogin.username} and password: {TestUserLogin.password} is currently allowed."
        # )

    return token


@app.get("/users/me")
async def read_users_me(user_id: str = Depends(get_user_id)) -> dict[str, str]:
    """
    Retrieve the current user's information based on the token.
    :param user_id: The ID of the authenticated user, or "unauthenticated_user" for unauthenticated requests.
    :return: A dictionary containing the user ID.
    """
    return {"user_id": user_id}


@app.get("/model_info")
async def model_info() -> dict[str, Any]:
    """
    Retrieve information about the AI model being used.
    :return: A dictionary containing model information.
    """
    if not ai_platform:
        raise HTTPException(
            status_code=500,
            detail="AI platform is not configured properly."
        )
    return ai_platform.get_model_info()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, user_id: Optional[str] = Depends(get_user_id)):
    """
    Handle chat requests by processing the user's prompt and returning a response from the AI model.
    :param request: The chat request containing the user's prompt.
    :param user_id: The ID of the authenticated user, or "unauthenticated_user" for unauthenticated requests.
    :return: A ChatResponse containing the AI-generated response.
    """
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty."
        )
    if len(request.prompt) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Prompt exceeds the maximum length of 1000 characters."
        )
    if not ai_platform:
        raise HTTPException(
            status_code=500,
            detail="AI platform is not configured properly."
        )

    # Validate user_id
    if not user_id:
        user_id = "unauthenticated_user"
    if not isinstance(user_id, str):
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID format."
        )

    # AI Interaction Logic
    # Apply rate limiting based on the prompt or user ID
    apply_rate_limit(user_id)
    response_text = ai_platform.chat(request.prompt)
    if response_text is None or not response_text.strip():
        response_text = "I'm sorry, I couldn't generate a response. Please try again later."

    return ChatResponse(response=response_text)
