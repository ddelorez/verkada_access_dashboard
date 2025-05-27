from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from ..db.session import get_db
from ..models import user as user_schemas
from ..services import user_service
from ..core import security
from ..db import models as db_models # Import db_models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/token") # Adjusted tokenUrl

async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> db_models.User:
    """
    Dependency to get the current user from a JWT token.
    - Decodes the token.
    - Retrieves the user from the database based on the username in the token.
    - Raises HTTPException if the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        if payload is None:
            raise credentials_exception
        
        # Ensure 'sub' exists in payload and is a string
        username_from_payload = payload.get("sub")
        if not isinstance(username_from_payload, str): # Check if it's a string
            raise credentials_exception
            
        # Now username_from_payload is confirmed to be a string
        token_data = user_schemas.TokenData(username=username_from_payload)

    except JWTError:
        raise credentials_exception
    
    # token_data.username is Optional[str], but get_user_by_username expects str.
    # We've already validated username_from_payload is a str, so token_data.username should be set.
    # However, to be absolutely safe for the type checker and runtime:
    if token_data.username is None: # This should ideally not happen given the logic above
        raise credentials_exception

    user = user_service.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: db_models.User = Depends(get_current_user)
) -> db_models.User:
    """
    Dependency to get the current active user.
    This can be expanded later to check if the user is active, e.g., not disabled.
    For now, it just returns the user obtained from get_current_user.
    """
    # if not current_user.is_active: # Example for future active check
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user