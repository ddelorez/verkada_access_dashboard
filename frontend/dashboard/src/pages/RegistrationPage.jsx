import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext'; // Import useAuth

function RegistrationPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState(''); // Email is collected but not sent to /register for now
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const { register, loading: authLoading } = useAuth(); // Get register function and loading state

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');

    if (password !== confirmPassword) {
      setError("Passwords don't match!");
      return;
    }

    // The context's register function only takes username and password
    const result = await register(username, password);

    if (result.success) {
      setSuccess('Registration successful! You can now try logging in.');
      // Form clearing is optional, depends on desired UX
      // setUsername('');
      // setEmail('');
      // setPassword('');
      // setConfirmPassword('');
    } else {
      setError(result.error || 'Registration failed. Please try again.');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="px-8 py-6 mt-4 text-left bg-white shadow-lg rounded-lg">
        <h3 className="text-2xl font-bold text-center">Create an account</h3>
        {error && <p className="mt-2 text-xs text-red-600 text-center">{error}</p>}
        {success && <p className="mt-2 text-xs text-green-600 text-center">{success}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mt-4">
            <div>
              <label className="block" htmlFor="username">Username</label>
              <input
                type="text"
                placeholder="Choose a username"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                required
                disabled={authLoading}
              />
            </div>
            <div className="mt-4">
              <label className="block" htmlFor="email">Email</label>
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
              {/* <p className="text-xs text-gray-500 mt-1">Email is for communication, not login.</p> */}
            </div>
            <div className="mt-4">
              <label className="block" htmlFor="password">Password</label>
              <input
                type="password"
                placeholder="Create a password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                required
                disabled={authLoading}
              />
            </div>
            <div className="mt-4">
              <label className="block" htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                placeholder="Confirm your password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
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
                {authLoading ? 'Registering...' : 'Register'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default RegistrationPage;