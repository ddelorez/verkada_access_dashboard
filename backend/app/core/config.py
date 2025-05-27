import os
from functools import lru_cache
from pydantic_settings import BaseSettings # For potential future typed settings

from .verkada_client.authenticator import VerkadaAuthenticator
from .verkada_client.exceptions import ApiKeyNotFoundError

class Settings(BaseSettings):
    """
    Application settings.
    Values are loaded from environment variables and .env file.
    """
    VERKADA_API_KEY: str = os.getenv("VERKADA_API_KEY", "not_set")
    VERKADA_ORG_ID: str = os.getenv("VERKADA_ORG_ID", "not_set") # If needed by authenticator or other services
    # Add other settings here as needed

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore" # Ignore extra fields from .env

@lru_cache() # Cache the result of this function
def get_settings() -> Settings:
    """Returns the application settings."""
    return Settings()

# Global Verkada Authenticator instance
# This will be initialized once and reused.
# It relies on VERKADA_API_KEY being available in the environment.
try:
    # Initialize with API key from settings/environment
    # The VerkadaAuthenticator itself loads from os.getenv if no key is passed,
    # but this makes the dependency on the env var explicit here.
    settings = get_settings()
    if settings.VERKADA_API_KEY == "not_set":
        # This check is a bit redundant if ApiKeyNotFoundError is handled well by VerkadaAuthenticator
        # but provides an early explicit error if the .env or env var is missing.
        raise ApiKeyNotFoundError("VERKADA_API_KEY is not set in environment or .env file.")
    
    # We can pass the API key directly, or let VerkadaAuthenticator pick it up from os.getenv
    # Passing it directly makes the dependency clearer.
    verkada_auth_client = VerkadaAuthenticator(api_key=settings.VERKADA_API_KEY)

except ApiKeyNotFoundError as e:
    print(f"CRITICAL ERROR: Could not initialize VerkadaAuthenticator: {e}")
    # In a real app, you might want to exit or prevent startup if this fails.
    # For now, we'll let it proceed, but API calls will fail.
    verkada_auth_client = None # type: ignore 
    # Set to None to indicate failure, or re-raise to stop app

# To use the authenticator in other modules:
# from ..core.config import verkada_auth_client
# if verkada_auth_client:
#     headers = verkada_auth_client.get_auth_headers()
# else:
#     # Handle case where authenticator failed to initialize