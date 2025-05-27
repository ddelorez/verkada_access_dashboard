"""
Core module for Verkada API authentication.
Provides the VerkadaAuthenticator class to manage API keys and tokens.
"""
import os
import requests
from datetime import datetime, timedelta, timezone
from typing import Optional
from dotenv import load_dotenv

from .exceptions import ApiKeyNotFoundError, TokenGenerationError

# Load environment variables from .env file
load_dotenv()

VERKADA_TOKEN_API_URL = "https://api.verkada.com/token"
TOKEN_VALIDITY_MINUTES = 30
# Using a slightly shorter duration for safety margin before actual expiry
TOKEN_CACHE_DURATION_MINUTES = TOKEN_VALIDITY_MINUTES - 1

class VerkadaAuthenticator:
    """
    Handles authentication with the Verkada API.

    Manages the Verkada API key and fetches short-lived API tokens,
    caching them for a predefined duration.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the VerkadaAuthenticator.

        Args:
            api_key (str, optional): The Verkada API key. If not provided,
                                     it attempts to load 'VERKADA_API_KEY'
                                     from environment variables.

        Raises:
            ApiKeyNotFoundError: If the API key is not provided and cannot be
                                 found in environment variables.
        """
        if api_key:
            self._api_key = api_key
        else:
            self._api_key = os.getenv("VERKADA_API_KEY")

        if not self._api_key:
            # Reason: API key is essential for authentication.
            raise ApiKeyNotFoundError(
                "VERKADA_API_KEY not found in environment variables or provided directly."
            )

        self._api_token: str | None = None
        self._token_expiry_time: datetime | None = None
        # Reason: Store the API URL as an instance variable for potential future flexibility,
        # though it's currently a constant.
        self._token_url: str = VERKADA_TOKEN_API_URL

    def _fetch_new_token(self) -> str:
        """
        Fetches a new API token from the Verkada token endpoint.

        Returns:
            str: The newly fetched API token.

        Raises:
            TokenGenerationError: If the token generation fails due to network
                                  issues or an error response from the API.
        """
        headers = {
            "accept": "application/json",
            "x-api-key": self._api_key
        }

        try:
            # Reason: Making the actual API call to Verkada.
            response = requests.post(self._token_url, headers=headers, timeout=10) # 10 second timeout
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
        except requests.exceptions.HTTPError as http_err:
            # Reason: Specific handling for HTTP errors from the API.
            raise TokenGenerationError(
                message=f"HTTP error occurred while fetching token: {http_err.response.status_code}",
                status_code=http_err.response.status_code,
                details=http_err.response.text
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            # Reason: Handling for other network-related issues.
            raise TokenGenerationError(
                message=f"Request exception occurred while fetching token: {req_err}"
            ) from req_err

        try:
            token_data = response.json()
            new_token = token_data.get("apiToken") # Based on cURL example, assuming "apiToken"
            if not new_token:
                # Reason: The expected token field is missing from the response.
                raise TokenGenerationError(
                    message="API token not found in response from Verkada.",
                    details=response.text
                )
        except ValueError as json_err: # Includes JSONDecodeError
            # Reason: The API response was not valid JSON.
            raise TokenGenerationError(
                message="Failed to decode JSON response from Verkada token API.",
                details=response.text
            ) from json_err

        self._api_token = new_token
        # Reason: Setting token expiry time with a safety margin.
        self._token_expiry_time = datetime.now(timezone.utc) + \
                                  timedelta(minutes=TOKEN_CACHE_DURATION_MINUTES)
        # Reason: Ensure token is not None after successful fetch and validation, satisfying type checker.
        # The new_token variable is checked for None before assignment to self._api_token.
        # If new_token were None, TokenGenerationError would have been raised.
        # Therefore, self._api_token is guaranteed to be a string here.
        assert self._api_token is not None, "API token should be a string after successful fetch."
        return self._api_token

    def get_api_token(self) -> str:
        """
        Retrieves a valid Verkada API token.

        If a cached token exists and is still valid, it's returned.
        Otherwise, a new token is fetched from the Verkada API.

        Returns:
            str: A valid Verkada API token.

        Raises:
            TokenGenerationError: If fetching a new token fails.
            ApiKeyNotFoundError: If the API key was not properly initialized.
        """
        # Reason: Ensure API key was set during initialization, though __init__ should prevent this.
        if not self._api_key:
            raise ApiKeyNotFoundError("Authenticator not properly initialized with an API key.")

        current_time = datetime.now(timezone.utc)
        # Reason: Check if cached token is still valid to avoid unnecessary API calls.
        if self._api_token and self._token_expiry_time and self._token_expiry_time > current_time:
            return self._api_token

        # Reason: Cached token is invalid or expired, fetch a new one.
        return self._fetch_new_token()

    def get_auth_headers(self) -> dict:
        """
        Generates the authorization headers required for Verkada API calls.

        This uses the short-lived API token.

        Returns:
            dict: A dictionary containing the 'x-verkada-auth' header.
        """
        api_token = self.get_api_token()
        return {"x-verkada-auth": api_token}