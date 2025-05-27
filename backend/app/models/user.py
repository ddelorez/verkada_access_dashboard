from pydantic import BaseModel, Field, ConfigDict # Import ConfigDict
from typing import Optional

class UserBase(BaseModel):
    """
    Base Pydantic model for User attributes.
    """
    username: str = Field(..., min_length=3, max_length=50, description="Unique username for the user")

class UserCreate(UserBase):
    """
    Pydantic model for creating a new user.
    Includes password.
    """
    password: str = Field(..., min_length=8, description="User's password")

class User(UserBase):
    """
    Pydantic model for representing a user (e.g., in API responses).
    Excludes password.
    """
    id: int
    model_config = ConfigDict(from_attributes=True) # Use model_config for Pydantic v2

class Token(BaseModel):
    """
    Pydantic model for representing an access token.
    """
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """
    Pydantic model for data stored within a JWT.
    """
    username: Optional[str] = None