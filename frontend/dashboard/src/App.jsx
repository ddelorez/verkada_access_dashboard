import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';
import ProtectedRoute from './components/ProtectedRoute';
import { useAuth } from './context/AuthContext';
import EventTimeline from './components/EventTimeline'; // Import EventTimeline
import EventFilters from './components/EventFilters'; // Import EventFilters
import PeakAccessChart from './components/PeakAccessChart'; // Import PeakAccessChart
import { useState } from 'react'; // Import useState
import './App.css'; // Keep existing App.css or remove if not needed for new layout

// Placeholder for Dashboard Page
function DashboardPage() {
  const { logout, user } = useAuth();
  const [filters, setFilters] = useState({ startDate: '', endDate: ''/*, user: ''*/ });

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };
  
  // Note: The user object in AuthContext is currently null.
  // It would need to be populated, e.g., by a fetchUser function after login.
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-xl font-semibold text-gray-700">Verkada Access Dashboard</h1>
          <div className="flex items-center">
            {user && <span className="text-gray-600 mr-4">Welcome, {user.username}!</span>}
            <button
              onClick={logout}
              className="px-4 py-2 text-sm text-white bg-red-500 rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-grow container mx-auto px-4 py-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Dashboard Overview</h2>
        <EventFilters onFilterChange={handleFilterChange} />
        <EventTimeline filters={filters} /> {/* Pass filters to EventTimeline */}
        <PeakAccessChart /> {/* Add PeakAccessChart component here */}
      </main>

      {/* Footer (Optional) */}
      <footer className="bg-gray-200 text-center p-4 text-sm text-gray-600">
        &copy; {new Date().getFullYear()} Verkada Dashboard Project
      </footer>
    </div>
  );
}

// Component to handle root navigation logic
function RootRedirector() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>; // Or some loading spinner
  }

  return isAuthenticated ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegistrationPage />} />
        
        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          {/* Add other protected routes here, e.g., /profile, /settings */}
        </Route>

        {/* Root path redirection logic */}
        <Route path="/" element={<RootRedirector />} />
        
        {/* Catch-all for 404 - redirects to root, which then decides where to go */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
