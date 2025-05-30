import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LoginPage from './LoginPage';
import { AuthContext } from '../context/AuthContext'; // To mock AuthContext

// Mock the AuthContext
const mockLogin = vi.fn();
const mockAuthContextValue = {
  login: mockLogin,
  loading: false,
  // Add other properties from AuthContext if LoginPage uses them
  user: null, 
  token: null,
  logout: vi.fn(),
  register: vi.fn(),
  // verkadaAuthStatus: null, 
  // checkVerkadaAuth: vi.fn(),
  // verkadaLogin: vi.fn(),
  // verkadaLogout: vi.fn(),
};

describe('LoginPage', () => {
  it('renders login form elements', () => {
    render(
      <AuthContext.Provider value={mockAuthContextValue}>
        <LoginPage />
      </AuthContext.Provider>
    );

    // Check for the heading
    expect(screen.getByRole('heading', { name: /login to your account/i })).toBeInTheDocument();

    // Check for email input (labeled "Email (as Username)")
    expect(screen.getByLabelText(/email \(as username\)/i)).toBeInTheDocument();
    
    // Check for password input
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();

    // Check for login button
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('calls login function on form submission', async () => {
    mockLogin.mockResolvedValue({ success: true }); // Mock a successful login

    render(
      <AuthContext.Provider value={mockAuthContextValue}>
        <LoginPage />
      </AuthContext.Provider>
    );

    const emailInput = screen.getByLabelText(/email \(as username\)/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const loginButton = screen.getByRole('button', { name: /login/i });

    // Simulate user input
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    // Simulate form submission
    fireEvent.click(loginButton);

    // Check if the login function from AuthContext was called
    expect(mockLogin).toHaveBeenCalledTimes(1);
    expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
    
    // Optionally, check for success message (if login is mocked to be successful)
    // await screen.findByText(/login successful! redirecting.../i); // Requires async findBy
  });

  // Add more tests:
  // - Error message display on failed login
  // - Button disabled state when authLoading is true
});