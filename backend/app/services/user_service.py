from sqlalchemy.orm import Session
from typing import Optional

from ..db import models as db_models
from ..models import user as user_schemas
from ..core.security import get_password_hash

def get_user_by_username(db: Session, username: str) -> Optional[db_models.User]:
    """
    Retrieves a user by their username.

    Args:
        db: The database session.
        username: The username to search for.

    Returns:
        The User database model instance if found, otherwise None.
    """
    return db.query(db_models.User).filter(db_models.User.username == username).first()

def get_user(db: Session, user_id: int) -> Optional[db_models.User]:
    """
    Retrieves a user by their ID.

    Args:
        db: The database session.
        user_id: The ID of the user to search for.

    Returns:
        The User database model instance if found, otherwise None.
    """
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()

def create_user(db: Session, user: user_schemas.UserCreate) -> db_models.User:
    """
    Creates a new user in the database.

    Args:
        db: The database session.
        user: The UserCreate schema containing user details (username, password).

    Returns:
        The created User database model instance.
    """
    hashed_password = get_password_hash(user.password)
    db_user = db_models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Additional CRUD operations (update, delete) can be added here later if needed.