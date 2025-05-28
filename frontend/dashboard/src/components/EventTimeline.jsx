import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext'; // To ensure auth headers are set by context

function EventTimeline({ filters }) { // Accept filters as a prop
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token } = useAuth(); // Access token to ensure it's available before fetching

  useEffect(() => {
    const fetchEvents = async () => {
      if (!token) {
        setLoading(false);
        setEvents([]); // Clear events if not authenticated
        return;
      }
      try {
        setLoading(true);
        setError(null);
        
        const queryParams = new URLSearchParams();
        if (filters?.startDate) {
          queryParams.append('start_date', filters.startDate);
        }
        if (filters?.endDate) {
          queryParams.append('end_date', filters.endDate);
        }
        // if (filters?.user) { // If user filter is implemented
        //   queryParams.append('user_id', filters.user);
        // }
        
        const endpoint = `/api/v1/verkada/events${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
        
        const response = await axios.get(endpoint);
        setEvents(response.data.data || response.data || []); // Ensure events is an array
        setLoading(false);
      } catch (err) {
        console.error("Failed to fetch events:", err);
        setError(err.response?.data?.detail || "Failed to load events.");
        setEvents([]); // Clear events on error
        setLoading(false);
      }
    };

    fetchEvents();
  }, [token, filters]); // Re-fetch if token or filters change

  if (loading) {
    return <div className="text-center p-4">Loading events...</div>;
  }

  if (error) {
    return <div className="text-center p-4 text-red-500">Error: {error}</div>;
  }

  if (events.length === 0) {
    return <div className="text-center p-4 text-gray-500">No events to display.</div>;
  }

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-700 mb-4">Access Events Timeline</h2>
      <ul className="space-y-4">
        {events.map((event) => (
          // TODO: Define a proper EventItem component or structure
          <li key={event.id || event.timestamp} className="p-3 bg-gray-50 rounded-md shadow-sm">
            <p className="font-medium text-gray-800">{event.description || JSON.stringify(event)}</p>
            <p className="text-sm text-gray-500">
              {new Date(event.timestamp).toLocaleString()} - User: {event.user_id || 'N/A'}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EventTimeline;