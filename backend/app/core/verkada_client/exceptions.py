"""Custom exceptions for the Verkada authentication module."""

class ApiKeyNotFoundError(Exception):
    """Raised when the Verkada API key is not found."""
    def __init__(self, message="Verkada API key not found in environment variables or direct input."):
        self.message = message
        super().__init__(self.message)

class TokenGenerationError(Exception):
    """Raised when there's an error generating an API token."""
    def __init__(self, message="Failed to generate Verkada API token.", status_code=None, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details
        full_message = f"{message}"
        if status_code:
            full_message += f" Status Code: {status_code}."
        if details:
            full_message += f" Details: {details}"
        super().__init__(full_message)