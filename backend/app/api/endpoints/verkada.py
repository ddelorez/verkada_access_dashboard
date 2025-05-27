from fastapi import APIRouter, Depends, HTTPException, status, Query # Added Query
from sqlalchemy.orm import Session
import requests
from typing import Any, List, Dict, Optional # Added Optional
from datetime import datetime, timedelta, timezone # Added datetime, timedelta, timezone
import pandas as pd # Import pandas

from ....app.core.config import verkada_auth_client, get_settings
from ....app.core.verkada_client.exceptions import TokenGenerationError, ApiKeyNotFoundError
from ....app.db.session import get_db # For consistency, though not used here yet
from ....app.core.dependencies import get_current_active_user # To protect this endpoint
from ....app.db import models as db_models # For type hinting current_user
from ....app.models import verkada_event as verkada_event_schemas # Import Verkada event Pydantic models


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

@router.get(
    "/events",
    response_model=verkada_event_schemas.VerkadaEventListResponse, # Placeholder response model
    summary="Get Access Control Events from Verkada"
)
async def get_verkada_access_events(
    params: verkada_event_schemas.VerkadaEventQueryParams = Depends(),
    current_user: db_models.User = Depends(get_current_active_user) # Protect the endpoint
):
    """
    Fetches access control events from the Verkada API.
    - Requires user authentication.
    - Uses query parameters for filtering and pagination.
    """
    if not verkada_auth_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Verkada authenticator is not initialized. Check API key configuration."
        )

    try:
        auth_headers = verkada_auth_client.get_auth_headers()
    except (ApiKeyNotFoundError, TokenGenerationError) as e:
        # Handle auth issues gracefully, similar to test-token endpoint
        detail_message = f"Verkada API Authentication error: {e}"
        if isinstance(e, TokenGenerationError):
            detail_message = f"Failed to generate Verkada API token: {e.message} (Status: {e.status_code}, Details: {e.details})"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, # Or 500 depending on error type
            detail=detail_message
        )

    # Construct the Verkada API URL
    settings = get_settings()
    # Ensure the base URL from settings does not end with a slash, and the path does not start with one.
    base_url = settings.VERKADA_API_BASE_URL.rstrip('/')
    api_path = "events/v1/access" # Path from Verkada documentation
    verkada_events_url = f"{base_url}/{api_path}"

    # Prepare query parameters, excluding None values
    query_params = params.model_dump(exclude_none=True)

    try:
        response = requests.get(
            verkada_events_url,
            headers=auth_headers,
            params=query_params,
            timeout=15 # Increased timeout for potentially larger data
        )
        response.raise_for_status() # Raise an exception for HTTP error codes
        
        # TODO: Parse the actual response and map to VerkadaEventListResponse
        # For now, returning the raw JSON if successful
        # This will likely fail response_model validation until models are accurate
        response_data = response.json()
        
        # Placeholder mapping - this needs to be accurate based on actual API response
        # and the defined Pydantic models.
        # For now, returning a dummy response that matches the model structure
        # and attempting to parse what we expect.
        
        # Assuming the API response structure is like:
        # {
        #   "events": [ {event_data_1}, {event_data_2} ],
        #   "nextPageToken": "some_token_string_or_null"
        # }
        # We need to adjust VerkadaEvent model based on actual event_data structure.
        
        parsed_events = []
        raw_events = response_data.get("events", [])
        if isinstance(raw_events, list):
            for event_data_item in raw_events:
                try:
                    # This will fail if VerkadaEvent model doesn't match actual event_data_item
                    parsed_events.append(verkada_event_schemas.VerkadaEvent.model_validate(event_data_item))
                except Exception as parse_err:
                    # Log or handle individual event parsing errors if necessary
                    print(f"Error parsing event item: {event_data_item}, error: {parse_err}")
                    # Continue to parse other events or raise a more generic error

        # When instantiating the Pydantic model, use the actual field name.
        # The value comes from the JSON response, where the key is 'nextPageToken' (the alias).
        
        # Construct arguments for the Pydantic model explicitly
        response_args = {
            "events": parsed_events,
            "next_page_token": response_data.get("nextPageToken") # Use field name as key for args dict
        }
        return verkada_event_schemas.VerkadaEventListResponse(**response_args)

    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(
            status_code=http_err.response.status_code,
            detail=f"HTTP error from Verkada API: {http_err.response.text}"
        )
    except requests.exceptions.RequestException as req_err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Network error connecting to Verkada API: {req_err}"
        )
    except ValueError as json_err: # Includes JSONDecodeError
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to decode JSON response from Verkada events API: {response.text if 'response' in locals() else 'No response text'}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while fetching Verkada events: {str(e)}"
        )

async def _fetch_all_verkada_events(
    start_time_dt: datetime,
    end_time_dt: datetime,
    auth_headers: Dict[str, str],
    initial_params: Optional[Dict[str, Any]] = None
) -> List[verkada_event_schemas.VerkadaEvent]:
    """
    Helper function to fetch all Verkada events within a time range, handling pagination.
    """
    all_events: List[verkada_event_schemas.VerkadaEvent] = []
    
    settings = get_settings()
    base_url = settings.VERKADA_API_BASE_URL.rstrip('/')
    api_path = "events/v1/access"
    current_verkada_events_url = f"{base_url}/{api_path}"

    # Prepare initial query parameters
    current_query_params = {
        "start_time": int(start_time_dt.timestamp()),
        "end_time": int(end_time_dt.timestamp()),
        "page_size": 200 # Max page size
    }
    if initial_params:
        current_query_params.update(initial_params)

    page_count = 0 # Safety break for pagination
    max_pages = 20 # Fetch a maximum of 20 pages (20 * 200 = 4000 events) to prevent accidental long runs

    while current_verkada_events_url and page_count < max_pages:
        page_count += 1
        try:
            response = requests.get(
                current_verkada_events_url, # For subsequent calls, this might be just the base + path
                headers=auth_headers,
                params=current_query_params, # Pass current_query_params here
                timeout=15
            )
            response.raise_for_status()
            response_data = response.json()

            raw_events = response_data.get("events", [])
            if isinstance(raw_events, list):
                for event_data_item in raw_events:
                    try:
                        all_events.append(verkada_event_schemas.VerkadaEvent.model_validate(event_data_item))
                    except Exception as parse_err:
                        print(f"Error parsing event item during all_events fetch: {event_data_item}, error: {parse_err}")
            
            next_page_token = response_data.get("nextPageToken")
            if next_page_token:
                current_query_params["page_token"] = next_page_token
                # The URL itself doesn't change for subsequent paginated requests, only the page_token param
            else:
                break # No more pages

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error fetching all events page {page_count}: {http_err.response.text}")
            break # Stop pagination on error
        except requests.exceptions.RequestException as req_err:
            print(f"Network error fetching all events page {page_count}: {req_err}")
            break # Stop pagination on error
        except ValueError as json_err:
            print(f"JSON decode error fetching all events page {page_count}: {response.text if 'response' in locals() else 'No response text'}")
            break
        except Exception as e:
            print(f"Unexpected error fetching all events page {page_count}: {str(e)}")
            break
            
    return all_events

@router.get(
    "/peak-times",
    response_model=verkada_event_schemas.PeakTimesResponse,
    summary="Get Peak Access Times from Verkada Events"
)
async def get_verkada_peak_times(
    current_user: db_models.User = Depends(get_current_active_user),
    # Add query params for time range if needed, e.g., last_n_days
    days_history: int = Query(default=7, ge=1, le=30, description="Number of past days to analyze for peak times (1-30).")
):
    """
    Analyzes Verkada access events to determine peak access times.
    - Fetches events for the specified number of past days.
    - Aggregates event counts by hour of the day.
    """
    if not verkada_auth_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Verkada authenticator not initialized."
        )

    try:
        auth_headers = verkada_auth_client.get_auth_headers()
    except (ApiKeyNotFoundError, TokenGenerationError) as e:
        # Simplified error handling for brevity
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Verkada Auth error: {e}")

    end_time_dt = datetime.now(timezone.utc)
    start_time_dt = end_time_dt - timedelta(days=days_history)

    # Fetch all events for the period
    # We might want to pass specific event_types if only certain events contribute to "peak times"
    all_events = await _fetch_all_verkada_events(start_time_dt, end_time_dt, auth_headers)

    if not all_events:
        return verkada_event_schemas.PeakTimesResponse(
            data=[],
            time_range_start=start_time_dt,
            time_range_end=end_time_dt
        )

    # Process with Pandas
    try:
        df = pd.DataFrame([event.model_dump() for event in all_events])
        if 'timestamp' not in df.columns or df.empty:
             return verkada_event_schemas.PeakTimesResponse(data=[], time_range_start=start_time_dt, time_range_end=end_time_dt)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        
        peak_times_counts = df.groupby('hour').size().reset_index(name='event_count')
        
        # Ensure all hours from 0-23 are present, filling missing with 0
        all_hours_df = pd.DataFrame({'hour': range(24)})
        peak_times_counts = pd.merge(all_hours_df, peak_times_counts, on='hour', how='left').fillna(0)
        peak_times_counts['event_count'] = peak_times_counts['event_count'].astype(int)

        peak_time_data_points = [
            verkada_event_schemas.PeakTimeDataPoint(hour=row['hour'], event_count=row['event_count'])
            for index, row in peak_times_counts.iterrows()
        ]
        
        return verkada_event_schemas.PeakTimesResponse(
            data=peak_time_data_points,
            time_range_start=start_time_dt,
            time_range_end=end_time_dt
        )
    except Exception as e:
        # Log the error for debugging
        print(f"Error processing events with Pandas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing event data: {str(e)}"
        )

# Add other Verkada related endpoints here, e.g., for fetching events.