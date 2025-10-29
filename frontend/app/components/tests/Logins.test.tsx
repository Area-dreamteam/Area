/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Logins component unit tests
*/

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Logins from '../Logins';

// Mock next/navigation
const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
}));

// Mock next/link
jest.mock('next/link', () => {
  return ({ children, href, ...props }: { children: React.ReactNode; href: string; [key: string]: unknown }) => {
    return <a href={href} {...props}>{children}</a>;
  };
});

// Mock UI components
jest.mock('@/components/ui/alert', () => ({
  Alert: ({ children, variant, className }: { children: React.ReactNode; variant?: string; className?: string }) => (
    <div data-testid="alert" className={`alert ${variant} ${className}`}>
      {children}
    </div>
  ),
  AlertDescription: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="alert-description">{children}</div>
  ),
  AlertTitle: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="alert-title">{children}</div>
  ),
}));

jest.mock('lucide-react', () => ({
  AlertCircleIcon: () => <div data-testid="alert-circle-icon">!</div>,
}));

// Mock Forms components
jest.mock('../Forms', () => ({
  Mail: ({ onChange }: { onChange?: (value: string) => void }) => (
    <input
      type="email"
      onChange={(e) => onChange?.(e.target.value)}
      data-testid="mail-input"
      placeholder="Email"
    />
  ),
  Password: ({ onChange }: { onChange?: (value: string) => void }) => (
    <input
      type="password"
      onChange={(e) => onChange?.(e.target.value)}
      data-testid="password-input"
      placeholder="Password"
    />
  ),
}));

// Mock functions
jest.mock('../../functions/fetch', () => ({
  fetchLogin: jest.fn(),
  fetchRegister: jest.fn(),
}));

jest.mock('../../functions/oauth', () => ({
  fetchAvailableOAuth: jest.fn(),
  redirectOauth: jest.fn(),
}));

// Get mocked functions for assertions
const mockFetchLogin = jest.requireMock('../../functions/fetch').fetchLogin;
const mockFetchRegister = jest.requireMock('../../functions/fetch').fetchRegister;
const mockFetchAvailableOAuth = jest.requireMock('../../functions/oauth').fetchAvailableOAuth;
const mockRedirectOauth = jest.requireMock('../../functions/oauth').redirectOauth;

describe('Logins Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockFetchAvailableOAuth.mockImplementation((setLogins: (logins: { name: string }[]) => void) => {
      setLogins([
        { name: 'Google' },
        { name: 'GitHub' },
      ]);
    });
  });

  describe('Login Mode', () => {
    it('renders login form with correct elements', async () => {
      render(<Logins isRegister={false} />);
      
      expect(screen.getByText('Area')).toBeInTheDocument();
      expect(screen.getByRole('heading', { name: 'Log in' })).toBeInTheDocument();
      expect(screen.getByTestId('mail-input')).toBeInTheDocument();
      expect(screen.getByTestId('password-input')).toBeInTheDocument();
      const submitButton = screen.getByRole('button', { name: /log in/i });
      expect(submitButton).toBeInTheDocument();
    });

    it('renders forgot password link in login mode', () => {
      render(<Logins isRegister={false} />);
      
      const forgotPasswordLink = screen.getByText('Forgot your password ?');
      expect(forgotPasswordLink.closest('a')).toHaveAttribute('href', '/passwords/forgot');
    });

    it('renders sign up link in login mode', () => {
      render(<Logins isRegister={false} />);
      
      expect(screen.getByText('New to Area ?')).toBeInTheDocument();
      const signUpLink = screen.getByText('Sign up here.');
      expect(signUpLink.closest('a')).toHaveAttribute('href', '/register');
    });

    it('handles successful login', async () => {
      mockFetchLogin.mockResolvedValue(true);
      render(<Logins isRegister={false} />);
      
      const emailInput = screen.getByTestId('mail-input');
      const passwordInput = screen.getByTestId('password-input');
      const submitButton = screen.getByRole('button', { name: /log in/i });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(mockFetchLogin).toHaveBeenCalledWith('test@example.com', 'password123');
        expect(mockPush).toHaveBeenCalledWith('/explore');
      });
    });

    it('handles failed login and shows error', async () => {
      mockFetchLogin.mockResolvedValue(false);
      render(<Logins isRegister={false} />);
      
      const emailInput = screen.getByTestId('mail-input');
      const passwordInput = screen.getByTestId('password-input');
      const submitButton = screen.getByRole('button', { name: /log in/i });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(mockFetchLogin).toHaveBeenCalledWith('test@example.com', 'wrongpassword');
        expect(screen.getByTestId('alert')).toBeInTheDocument();
        expect(screen.getByTestId('alert-title')).toHaveTextContent('Logins incorrect');
        expect(screen.getByTestId('alert-description')).toHaveTextContent('Your email or password seems to be wrong. Please try again.');
      });
    });
  });

  describe('Register Mode', () => {
    it('renders register form with correct elements', () => {
      render(<Logins isRegister={true} />);
      
      expect(screen.getByText('Area')).toBeInTheDocument();
      expect(screen.getByText('Register')).toBeInTheDocument();
      expect(screen.getByTestId('mail-input')).toBeInTheDocument();
      expect(screen.getByTestId('password-input')).toBeInTheDocument();
      expect(screen.getByText('Get started')).toBeInTheDocument();
    });

    it('does not render forgot password link in register mode', () => {
      render(<Logins isRegister={true} />);
      
      expect(screen.queryByText('Forgot your password ?')).not.toBeInTheDocument();
    });

    it('renders login link in register mode', () => {
      render(<Logins isRegister={true} />);
      
      expect(screen.getByText('Already have an account ?')).toBeInTheDocument();
      const loginLink = screen.getByText('Log in here.');
      expect(loginLink.closest('a')).toHaveAttribute('href', '/login');
    });

     it('handles successful registration', async () => {
       mockFetchRegister.mockResolvedValue(true);
       render(<Logins isRegister={true} />);
       
       const emailInput = screen.getByTestId('mail-input');
       const passwordInput = screen.getByTestId('password-input');
       const submitButton = screen.getByText('Get started');
       
       fireEvent.change(emailInput, { target: { value: 'newuser@example.com' } });
       fireEvent.change(passwordInput, { target: { value: 'SecurePass123!' } });
       fireEvent.click(submitButton);
       
       await waitFor(() => {
         expect(mockFetchRegister).toHaveBeenCalledWith('newuser@example.com', 'SecurePass123!');
         expect(mockPush).toHaveBeenCalledWith('/explore');
       });
     });

    it('handles failed registration and shows error', async () => {
      mockFetchRegister.mockResolvedValue(false);
      render(<Logins isRegister={true} />);
      
      const emailInput = screen.getByTestId('mail-input');
      const passwordInput = screen.getByTestId('password-input');
      const submitButton = screen.getByText('Get started');
      
      fireEvent.change(emailInput, { target: { value: 'existing@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(mockFetchRegister).toHaveBeenCalledWith('existing@example.com', 'password123');
        expect(screen.getByTestId('alert')).toBeInTheDocument();
        expect(screen.getByTestId('alert-title')).toHaveTextContent('Sorry, this account already exist');
      });
    });
  });

  describe('OAuth Integration', () => {
    it('loads and displays OAuth options', async () => {
      render(<Logins isRegister={false} />);
      
      await waitFor(() => {
        expect(mockFetchAvailableOAuth).toHaveBeenCalled();
        expect(screen.getByText('Continue with Google')).toBeInTheDocument();
        expect(screen.getByText('Continue with GitHub')).toBeInTheDocument();
      });
    });

     it('handles OAuth button clicks', async () => {
       render(<Logins isRegister={false} />);
       
       await waitFor(() => {
         const googleButton = screen.getByText('Continue with Google');
         fireEvent.click(googleButton);
         expect(mockRedirectOauth).toHaveBeenCalledWith('Google', '/explore');
       });
     });

    it('displays "Or" separator between form and OAuth options', () => {
      render(<Logins isRegister={false} />);
      
      expect(screen.getByText('Or')).toBeInTheDocument();
    });
  });

  describe('Form Validation', () => {
    it('handles form submission correctly', async () => {
      mockFetchLogin.mockResolvedValue(false);
      render(<Logins isRegister={false} />);
      
      const emailInput = screen.getByTestId('mail-input');
      const submitButton = screen.getByRole('button', { name: /log in/i });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(mockFetchLogin).toHaveBeenCalled();
      });
    });
  });
});