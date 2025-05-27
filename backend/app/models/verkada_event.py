from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class VerkadaEventQueryParams(BaseModel):
    """
    Pydantic model for query parameters when fetching Verkada access events.
    """
    start_time: Optional[int] = Field(None, description="Unix timestamp in seconds for the start of the time range.")
    end_time: Optional[int] = Field(None, description="Unix timestamp in seconds for the end of the time range.")
    page_token: Optional[str] = Field(None, description="Pagination token for the next page of results.")
    page_size: Optional[int] = Field(default=100, ge=1, le=200, description="Number of items per page (1-200).")
    event_type: Optional[str] = Field(None, description="Comma-separated list of event types to filter by.")
    site_id: Optional[str] = Field(None, description="Comma-separated list of site IDs to filter by.")
    device_id: Optional[str] = Field(None, description="Comma-separated list of device IDs to filter by.")
    user_id: Optional[str] = Field(None, description="Comma-separated list of user IDs to filter by.")

class VerkadaEvent(BaseModel):
    """
    Pydantic model representing a single Verkada access event.
    """
    event_id: str = Field(..., alias="eventId")
    event_type: str = Field(..., alias="eventType")
    timestamp: datetime 
    user_name: Optional[str] = Field(None, alias="userName")
    door_name: Optional[str] = Field(None, alias="doorName")
    # Add other relevant fields if needed from actual API response, e.g.:
    # device_id: Optional[str] = Field(None, alias="deviceId")
    # org_id: Optional[int] = Field(None, alias="orgId")
    # person_id: Optional[str] = Field(None, alias="personId")
    # credential_id: Optional[str] = Field(None, alias="credentialId")

    class Config:
        populate_by_name = True
        from_attributes = True

class VerkadaEventListResponse(BaseModel):
    """
    Pydantic model for the list response when fetching Verkada access events.
    """
    events: List[VerkadaEvent]
    next_page_token: Optional[str] = Field(None, alias="nextPageToken")

    class Config:
        populate_by_name = True
        from_attributes = True

class PeakTimeDataPoint(BaseModel):
    """
    Represents a data point for the peak times chart.
    e.g., hour of the day and the count of events during that hour.
    """
    hour: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    event_count: int = Field(..., ge=0, description="Number of events during this hour")

class PeakTimesResponse(BaseModel):
    """
    Pydantic model for the response of the peak access times endpoint.
    """
    data: List[PeakTimeDataPoint]
    time_range_start: Optional[datetime] = Field(None, description="Start of the time range analyzed")
    time_range_end: Optional[datetime] = Field(None, description="End of the time range analyzed")