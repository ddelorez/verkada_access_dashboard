import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext'; // Import useAuth

function LoginPage() {
  const [email, setEmail] = useState(''); // This will be used as 'username' for the backend
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const { login, loading: authLoading } = useAuth(); // Get login function and loading state

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');

    // Email state is used as username for the login function from context
    const result = await login(email, password);

    if (result.success) {
      setSuccess('Login successful! Redirecting...');
      // Token storage and global state update are handled by AuthContext
      // TODO: Implement redirection, e.g., using useNavigate from react-router-dom
      // navigate('/dashboard');
    } else {
      setError(result.error || 'Login failed. Please try again.');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="px-8 py-6 mt-4 text-left bg-white shadow-lg rounded-lg">
        <h3 className="text-2xl font-bold text-center">Login to your account</h3>
        {error && <p className="mt-2 text-xs text-red-600 text-center">{error}</p>}
        {success && <p className="mt-2 text-xs text-green-600 text-center">{success}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mt-4">
            <div>
              <label className="block" htmlFor="email">Email (as Username)</label>
              <input
                type="email"
                placeholder="your@email.com"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                required
                disabled={authLoading}
              />
            </div>
            <div className="mt-4">
              <label className="block" htmlFor="password">Password</label>
              <input
                type="password"
                placeholder="Password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                required
                disabled={authLoading}
              />
            </div>
            <div className="flex items-baseline justify-between">
              <button
                type="submit"
                className="px-6 py-2 mt-4 text-white bg-blue-600 rounded-lg hover:bg-blue-900 w-full disabled:opacity-50"
                disabled={authLoading}
              >
                {authLoading ? 'Logging in...' : 'Login'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;