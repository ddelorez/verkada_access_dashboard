import React, { useState } from 'react';

function EventFilters({ onFilterChange }) {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  // const [userFilter, setUserFilter] = useState(''); // Placeholder for user filter

  const handleApplyFilters = () => {
    // Basic validation: ensure dates are reasonable if needed
    onFilterChange({
      startDate,
      endDate,
      // user: userFilter,
    });
  };

  const handleClearFilters = () => {
    setStartDate('');
    setEndDate('');
    // setUserFilter('');
    onFilterChange({
      startDate: '',
      endDate: '',
      // user: '',
    });
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-6">
      <h3 className="text-lg font-semibold text-gray-700 mb-3">Filter Events</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
        <div>
          <label htmlFor="startDate" className="block text-sm font-medium text-gray-600 mb-1">
            Start Date
          </label>
          <input
            type="date"
            id="startDate"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="endDate" className="block text-sm font-medium text-gray-600 mb-1">
            End Date
          </label>
          <input
            type="date"
            id="endDate"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        {/* 
        <div>
          <label htmlFor="userFilter" className="block text-sm font-medium text-gray-600 mb-1">
            User
          </label>
          <input
            type="text"
            id="userFilter"
            placeholder="Enter username or ID"
            value={userFilter}
            onChange={(e) => setUserFilter(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        */}
        <div className="md:col-span-1 flex space-x-2">
          <button
            onClick={handleApplyFilters}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          >
            Apply
          </button>
          <button
            onClick={handleClearFilters}
            className="w-full bg-gray-300 hover:bg-gray-400 text-gray-700 font-semibold py-2 px-4 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-opacity-50"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}

export default EventFilters;