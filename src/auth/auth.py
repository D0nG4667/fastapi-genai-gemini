import os
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from ..schemas.pydantic import Token


# --- Constants ---
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable must be set.")

# --- OAuth2 Password Bearer for token authentication ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extract user ID from the JWT token.

    :param token: The JWT token provided in the request.
    :return: The user ID extracted from the token.
    :raises HTTPException: If the token is invalid or expired.
    """
    if not token:
        return "unauthenticated_user"  # Default for unauthenticated users

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the token: {str(e)}"
        )
    return user_id


async def create_jwt_token(user_id: str, expires_delta: Optional[timedelta] = None, token_type: str = 'Bearer') -> Token:
    """
    Create a JWT token for the given user ID.

    :param user_id: The ID of the user for whom the token is being created.
    :param expires_delta: Optional expiration time for the token.
    :return: A JWT token as a string.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=30)  # Default expiration time

    to_encode = {"sub": user_id, "exp": datetime.now(
        timezone.utc) + expires_delta}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    token = {
        "access_token": encoded_jwt,
        "token_type": token_type,
        "expires_in": expires_delta,
    }
    return Token(**token)
