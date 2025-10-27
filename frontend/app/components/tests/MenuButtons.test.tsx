/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** MenuButtons unit tests
*/

import { render, screen } from '@testing-library/react';
import MenuButton from '../MenuButtons';
import { NavigationMenu, NavigationMenuList } from '@radix-ui/react-navigation-menu';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  redirect: jest.fn(),
}));

// Mock next/link
jest.mock('next/link', () => {
  return ({ children, href, ...props }: { children: React.ReactNode; href: string; [key: string]: unknown }) => {
    return <a href={href} {...props}>{children}</a>;
  };
});

// Mock UI components
jest.mock('@/components/ui/navigation-menu', () => ({
  NavigationMenuItem: ({ children }: { children: React.ReactNode }) => <li>{children}</li>,
  NavigationMenuLink: ({ children, ...props }: { children: React.ReactNode; [key: string]: unknown }) => <div {...props}>{children}</div>,
}));

describe('MenuButton', () => {
  it('renders with correct text and link', () => {    
    const linkElement = screen.getByRole('link');
    const textElement = screen.getByText('Home');
    
    expect(textElement).toBeInTheDocument();
    expect(linkElement).toHaveAttribute('href', '/home');
  });

  it('renders with different text and link combinations', () => {
    render(MenuButton('About', '/about'));
    
    const linkElement = screen.getByRole('link');
    const textElement = screen.getByText('About');
    
    expect(textElement).toBeInTheDocument();
    expect(linkElement).toHaveAttribute('href', '/about');
  });

  it('applies correct styling classes', () => {
    render(MenuButton('Test', '/test'));
    
    const linkElement = screen.getByText('Test');
    expect(linkElement).toHaveClass('text-center');
  });

  it('renders within NavigationMenuItem wrapper', () => {
    const { container } = render(MenuButton('Test', '/test'));
    
    const listItem = container.querySelector('li');
    expect(listItem).toBeInTheDocument();
  });
});