/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** MenuButtons unit tests
*/

import { render, screen } from '@testing-library/react';
import MenuButton from '../MenuButtons';

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
  NavigationMenuLink: ({ children, asChild, ...props }: { children: React.ReactNode; asChild?: boolean; [key: string]: unknown }) => (
    <div {...props}>{children}</div>
  ),
}));

describe('MenuButton Component', () => {
  it('renders menu button with text and link', () => {
    render(MenuButton('Test Button', '/test-page'));
    expect(screen.getByRole('link')).toHaveAttribute('href', '/test-page');
    expect(screen.getByText('Test Button')).toBeInTheDocument();
  });
});
