from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    Database model for a User.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# Add other models here as needed, e.g., for audit logs or other entities.