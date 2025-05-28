import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function PeakAccessChart() {
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token } = useAuth();

  useEffect(() => {
    const fetchPeakTimesData = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        setError(null);
        // Assuming the endpoint is /api/v1/verkada/peak-times
        const response = await axios.get('/api/v1/verkada/peak-times');
        // TODO: Transform response.data into the format expected by Recharts
        // Example: [{ hour: '00:00', count: 10 }, { hour: '01:00', count: 15 }, ...]
        // For now, assuming response.data is already in a suitable array format
        setChartData(response.data.data || response.data || []); 
        setLoading(false);
      } catch (err) {
        console.error("Failed to fetch peak times data:", err);
        setError(err.response?.data?.detail || "Failed to load chart data.");
        setChartData([]);
        setLoading(false);
      }
    };

    fetchPeakTimesData();
  }, [token]);

  if (loading) {
    return <div className="text-center p-4">Loading chart data...</div>;
  }

  if (error) {
    return <div className="text-center p-4 text-red-500">Error: {error}</div>;
  }

  if (chartData.length === 0) {
    return <div className="text-center p-4 text-gray-500">No data available for chart.</div>;
  }

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mt-6">
      <h2 className="text-xl font-semibold text-gray-700 mb-4">Peak Access Times</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="hour" /> {/* Assuming data has 'hour' field for X-axis */}
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#8884d8" /> {/* Assuming data has 'count' field for Bar values */}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PeakAccessChart;