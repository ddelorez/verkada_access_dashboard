from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Though not used in this example, good for consistency

from ....app.core.config import verkada_auth_client # Import our shared client
from ....app.core.verkada_client.exceptions import TokenGenerationError, ApiKeyNotFoundError
from ....app.db.session import get_db # For consistency, though not used here yet
from ....app.core.dependencies import get_current_active_user # To protect this endpoint
from ....app.db import models as db_models # For type hinting current_user

router = APIRouter()

@router.get("/test-token", summary="Test Verkada API Token Retrieval")
async def test_verkada_token(current_user: db_models.User = Depends(get_current_active_user)):
    """
    Tests the retrieval of a Verkada API token using the VerkadaAuthenticator.
    This is a protected endpoint and requires user authentication.
    """
    if not verkada_auth_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Verkada authenticator is not initialized. Check API key configuration."
        )
    try:
        # Attempt to get the authentication headers
        # This will trigger a token fetch if one is not cached or is expired.
        auth_headers = verkada_auth_client.get_auth_headers()
        
        # For testing, we can just return a success message and part of the token
        # or the headers. Avoid returning the full token in a real non-debug endpoint.
        return {
            "message": "Successfully retrieved Verkada auth headers.",
            "x-verkada-auth-prefix": auth_headers.get("x-verkada-auth", "")[:10] + "..." if auth_headers.get("x-verkada-auth") else "Not found"
            # "full_token_for_debug": auth_headers.get("x-verkada-auth") # Uncomment for debugging only
        }
    except ApiKeyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verkada API Key not found: {e}"
        )
    except TokenGenerationError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to generate Verkada API token: {e.message} (Status: {e.status_code}, Details: {e.details})"
        )
    except Exception as e:
        # Catch any other unexpected errors during token retrieval
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while fetching Verkada token: {str(e)}"
        )

# Add other Verkada related endpoints here, e.g., for fetching events.