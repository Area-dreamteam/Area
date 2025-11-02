/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** BackButton unit tests
 */

import { render, screen, fireEvent } from '@testing-library/react'
import BackButton from '../Back'

// Mock next/navigation
const mockRouter = {
  back: jest.fn(),
  push: jest.fn(),
}

jest.mock('next/navigation', () => ({
  useRouter: () => mockRouter,
}))

// Mock UI components
jest.mock('@/components/ui/button', () => ({
  Button: ({
    children,
    onClick,
    className,
  }: {
    children: React.ReactNode
    onClick?: () => void
    className?: string
  }) => (
    <button onClick={onClick} className={className}>
      {children}
    </button>
  ),
}))

describe('BackButton', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders with correct text', () => {
    render(<BackButton />)

    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()
    expect(button).toHaveTextContent('ᐸ Back')
  })

  it('calls router.back() when clicked without dir prop', () => {
    render(<BackButton />)

    const button = screen.getByRole('button')
    fireEvent.click(button)

    expect(mockRouter.back).toHaveBeenCalledTimes(1)
    expect(mockRouter.push).not.toHaveBeenCalled()
  })

  it('calls router.push() when clicked with dir prop', () => {
    render(<BackButton dir="/home" />)

    const button = screen.getByRole('button')
    fireEvent.click(button)

    expect(mockRouter.push).toHaveBeenCalledWith('/home')
    expect(mockRouter.back).not.toHaveBeenCalled()
  })

  it('calls router.back() when dir is null', () => {
    render(<BackButton dir={null} />)

    const button = screen.getByRole('button')
    fireEvent.click(button)

    expect(mockRouter.back).toHaveBeenCalledTimes(1)
    expect(mockRouter.push).not.toHaveBeenCalled()
  })

  it('applies correct CSS classes', () => {
    render(<BackButton />)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('rounded-full')
    expect(button).toHaveClass('border-white')
    expect(button).toHaveClass('hover:bg-transparent')
    expect(button).toHaveClass('bg-transparent')
    expect(button).toHaveClass('border-[4px]')
    expect(button).toHaveClass('hover:cursor-pointer')
  })
})
