from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional # Import Optional

# Corrected relative imports
from ...models import user as user_schemas
from ...services import user_service
from ...db.session import get_db
from ...core import security
from ...db import models as db_models # Import db_models for explicit type hinting and querying
from ...core.dependencies import get_current_active_user # Import the dependency

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = security.ACCESS_TOKEN_EXPIRE_MINUTES

@router.post("/register", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
async def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.
    - Checks if a user with the given username already exists.
    - Creates the user if not.
    """
    db_user = user_service.get_user_by_username(db, username=user.username) # Corrected service call
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    created_user = user_service.create_user(db=db, user=user) # Corrected service call
    return created_user

@router.post("/login/token", response_model=user_schemas.Token)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Provides an access token for a user upon successful authentication.
    - Authenticates the user based on username and password.
    - Creates and returns a JWT access token.
    """
    # Explicitly type hint 'user' to help Pylance
    user: Optional[db_models.User] = user_service.get_user_by_username(db, username=form_data.username)
    
    if not user: # Check for user existence first
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Now 'user' is definitely a db_models.User instance
    # Add an assertion to help Pylance with type inference
    assert isinstance(user, db_models.User), "User should be an instance of db_models.User at this point"
    if not security.verify_password(form_data.password, str(user.hashed_password)): # Explicitly cast to str
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Placeholder for a protected endpoint to test authentication
# We will create the get_current_active_user dependency shortly.
# For now, let's comment out the Depends part to avoid an immediate error.
@router.get("/users/me", response_model=user_schemas.User)
async def read_users_me(current_user: db_models.User = Depends(get_current_active_user)): # Use the dependency
    """
    Fetches the current authenticated user.
    """
    # The current_user is already a db_models.User instance from the dependency
    # We need to convert it to the Pydantic schema for the response
    return user_schemas.User.model_validate(current_user)