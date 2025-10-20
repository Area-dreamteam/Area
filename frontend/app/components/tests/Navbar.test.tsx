/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Navbar components unit tests
*/

import { render, screen, fireEvent } from '@testing-library/react';
import NavigationBar, { ConnectedNavbar } from '../Navbar';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  redirect: jest.fn(),
}));

const { redirect: mockRedirect } = jest.requireMock('next/navigation');

// Mock next/link
jest.mock('next/link', () => {
  return ({ children, href, ...props }: { children: React.ReactNode; href: string; [key: string]: unknown }) => {
    return <a href={href} {...props}>{children}</a>;
  };
});

// Mock MenuButton component
jest.mock('../MenuButtons', () => {
  return jest.fn((text: string, linkedPage: string) => (
    <div data-testid={`menu-button-${text.toLowerCase().replace(/\s+/g, '-')}`}>
      <a href={linkedPage}>{text}</a>
    </div>
  ));
});

// Mock UI components
jest.mock('@/components/ui/navigation-menu', () => ({
  NavigationMenu: ({ children, className }: { children: React.ReactNode; className?: string }) => <nav className={className}>{children}</nav>,
  NavigationMenuList: ({ children, className }: { children: React.ReactNode; className?: string }) => <ul className={className}>{children}</ul>,
}));

jest.mock('@/components/ui/button', () => ({
  Button: ({ children, onClick, variant, className }: { children: React.ReactNode; onClick?: () => void; variant?: string; className?: string }) => (
    <button onClick={onClick} className={`${variant} ${className}`}>
      {children}
    </button>
  ),
}));

jest.mock('@/components/ui/dropdown-menu', () => ({
  DropdownMenu: ({ children }: { children: React.ReactNode }) => <div data-testid="dropdown-menu">{children}</div>,
  DropdownMenuContent: ({ children, className, align }: { children: React.ReactNode; className?: string; align?: string }) => (
    <div className={className} data-align={align}>{children}</div>
  ),
  DropdownMenuGroup: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  DropdownMenuItem: ({ children, onClick, disabled, className }: { children: React.ReactNode; onClick?: () => void; disabled?: boolean; className?: string }) => (
    <div
      onClick={onClick}
      className={className}
      data-disabled={disabled}
      data-testid="dropdown-menu-item"
    >
      {children}
    </div>
  ),
  DropdownMenuShortcut: ({ children }: { children: React.ReactNode }) => <span>{children}</span>,
  DropdownMenuTrigger: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="dropdown-trigger">{children}</div>
  ),
}));

describe('NavigationBar', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders navigation menu with correct structure', () => {
    render(<NavigationBar />);
    
    const nav = screen.getByRole('navigation');
    expect(nav).toBeInTheDocument();
    expect(nav).toHaveClass('flex', 'flex-row-reverse');
  });

  it('renders menu buttons for Explore, Login, and Register', () => {
    render(<NavigationBar />);
    
    expect(screen.getByTestId('menu-button-explore')).toBeInTheDocument();
    expect(screen.getByTestId('menu-button-login')).toBeInTheDocument();
    expect(screen.getByTestId('menu-button-register')).toBeInTheDocument();
  });

  it('menu buttons have correct links', () => {
    render(<NavigationBar />);
    
    const exploreLink = screen.getByTestId('menu-button-explore').querySelector('a');
    const loginLink = screen.getByTestId('menu-button-login').querySelector('a');
    const registerLink = screen.getByTestId('menu-button-register').querySelector('a');
    
    expect(exploreLink).toHaveAttribute('href', '/explore');
    expect(loginLink).toHaveAttribute('href', '/login');
    expect(registerLink).toHaveAttribute('href', '/register');
  });
});

describe('ConnectedNavbar', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders with correct layout structure', () => {
    render(<ConnectedNavbar />);
    
    const container = screen.getByText('Area').closest('div');
    expect(container).toHaveClass('flex', 'justify-between');
  });

  it('renders Area logo with correct link', () => {
    render(<ConnectedNavbar />);
    
    const logoLink = screen.getByText('Area').closest('a');
    expect(logoLink).toBeInTheDocument();
    expect(logoLink).toHaveAttribute('href', '/explore');
    expect(logoLink).toHaveClass('font-bold', 'text-[35px]');
  });

  it('renders navigation menu buttons for authenticated user', () => {
    render(<ConnectedNavbar />);
    
    expect(screen.getByTestId('menu-button-create')).toBeInTheDocument();
    expect(screen.getByTestId('menu-button-my-applets')).toBeInTheDocument();
    expect(screen.getByTestId('menu-button-explore')).toBeInTheDocument();
  });

  it('renders dropdown menu with profile trigger', () => {
    render(<ConnectedNavbar />);
    
    const dropdown = screen.getByTestId('dropdown-menu');
    const trigger = screen.getByTestId('dropdown-trigger');
    
    expect(dropdown).toBeInTheDocument();
    expect(trigger).toBeInTheDocument();
  });

  it('dropdown contains all menu items', () => {
    render(<ConnectedNavbar />);
    
    const menuItems = screen.getAllByTestId('dropdown-menu-item');
    expect(menuItems).toHaveLength(9); // Create, My applets, Explore, Account, My services, Activity, Archive, Help, Log out
  });

  it('dropdown menu items have correct click handlers for enabled items', () => {
    render(<ConnectedNavbar />);
    
    const menuItems = screen.getAllByTestId('dropdown-menu-item');
    
    // Test Account menu item (should call redirect to /settings)
    const accountItem = menuItems.find(item => item.textContent?.includes('Account'));
    if (accountItem) {
      fireEvent.click(accountItem);
      expect(mockRedirect).toHaveBeenCalledWith('/settings');
    }

    // Test Help menu item
    const helpItem = menuItems.find(item => item.textContent?.includes('Help'));
    if (helpItem) {
      fireEvent.click(helpItem);
      expect(mockRedirect).toHaveBeenCalledWith('/help');
    }

    // Test Log out menu item
    const logoutItem = menuItems.find(item => item.textContent?.includes('Log out'));
    if (logoutItem) {
      fireEvent.click(logoutItem);
      expect(mockRedirect).toHaveBeenCalledWith('/');
    }
  });

  it('has disabled menu items', () => {
    render(<ConnectedNavbar />);
    
    const menuItems = screen.getAllByTestId('dropdown-menu-item');
    
    const disabledItems = menuItems.filter(item => item.getAttribute('data-disabled') === 'true');
    expect(disabledItems.length).toBeGreaterThan(0);
    
    // Check specific disabled items
    const myServicesItem = menuItems.find(item => item.textContent?.includes('My services'));
    const activityItem = menuItems.find(item => item.textContent?.includes('Activity'));
    const archiveItem = menuItems.find(item => item.textContent?.includes('Archive'));
    
    expect(myServicesItem).toHaveAttribute('data-disabled', 'true');
    expect(activityItem).toHaveAttribute('data-disabled', 'true');
    expect(archiveItem).toHaveAttribute('data-disabled', 'true');
  });

  it('navigation menu list is hidden on mobile', () => {
    render(<ConnectedNavbar />);
    
    const navigationList = screen.getByRole('list');
    expect(navigationList).toHaveClass('hidden', 'md:flex');
  });

  it('dropdown trigger button has correct styling', () => {
    render(<ConnectedNavbar />);
    
    const button = screen.getByRole('button');
    expect(button).toHaveTextContent(':::');
    expect(button).toHaveClass('outline');
  });
});