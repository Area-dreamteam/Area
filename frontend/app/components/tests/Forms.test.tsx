/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** Forms components unit tests
 */

import { render, screen, fireEvent, act } from '@testing-library/react'
import { Mail, Password } from '../Forms'

// Mock UI components
jest.mock('@/components/ui/input', () => ({
  Input: ({
    onChange,
    ...props
  }: {
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
    [key: string]: unknown
  }) => <input onChange={onChange} {...props} data-testid="input" />,
}))

// Mock react-icons
jest.mock('react-icons/ri', () => ({
  RiEyeFill: ({
    onClick,
    className,
  }: {
    onClick?: () => void
    className?: string
  }) => (
    <div onClick={onClick} className={className} data-testid="eye-visible">
      Eye Open
    </div>
  ),
  RiEyeOffFill: ({
    onClick,
    className,
  }: {
    onClick?: () => void
    className?: string
  }) => (
    <div onClick={onClick} className={className} data-testid="eye-hidden">
      Eye Closed
    </div>
  ),
}))

describe('Mail Component', () => {
  it('renders email input with correct attributes', () => {
    render(<Mail />)

    const input = screen.getByTestId('input')
    expect(input).toBeInTheDocument()
    expect(input).toHaveAttribute('type', 'email')
    expect(input).toHaveAttribute('placeholder', 'Email')
    expect(input).toHaveAttribute(
      'pattern',
      '[a-zA-Z0-9._\\-]+@[a-zA-Z0-9_\\-]+\\.[a-z]{2,}$'
    )
    expect(input).toHaveAttribute('required')
  })

  it('calls onChange callback when input value changes', () => {
    const mockOnChange = jest.fn()
    render(<Mail onChange={mockOnChange} />)

    const input = screen.getByTestId('input')
    fireEvent.change(input, { target: { value: 'test@example.com' } })

    expect(mockOnChange).toHaveBeenCalledWith('test@example.com')
  })

  it('works without onChange callback', () => {
    expect(() => {
      render(<Mail />)
      const input = screen.getByTestId('input')
      fireEvent.change(input, { target: { value: 'test@example.com' } })
    }).not.toThrow()
  })

  it('applies correct CSS classes', () => {
    render(<Mail />)

    const input = screen.getByTestId('input')
    expect(input).toHaveClass('text-black')
    expect(input).toHaveClass('h-[100%]')
    expect(input).toHaveClass('w-5/6')
    expect(input).toHaveClass('border-none')
  })
})

describe('Password Component', () => {
  it('renders password input with correct initial state', () => {
    render(<Password />)

    const input = screen.getByTestId('input')
    const eyeIcon = screen.getByTestId('eye-hidden')

    expect(input).toBeInTheDocument()
    expect(input).toHaveAttribute('type', 'password')
    expect(input).toHaveAttribute('placeholder', 'Password')
    expect(input).toHaveAttribute('required')
    expect(eyeIcon).toBeInTheDocument()
  })

  it('toggles password visibility when eye icon is clicked', async () => {
    render(<Password />)

    // Initially hidden
    let eyeIcon = screen.getByTestId('eye-hidden')
    let input = screen.getByTestId('input')
    expect(input).toHaveAttribute('type', 'password')

    // Click to show password
    await act(async () => {
      fireEvent.click(eyeIcon)
    })

    eyeIcon = screen.getByTestId('eye-visible')
    input = screen.getByTestId('input')
    expect(input).toHaveAttribute('type', 'text')
    expect(eyeIcon).toBeInTheDocument()

    // Click to hide password again
    await act(async () => {
      fireEvent.click(eyeIcon)
    })

    eyeIcon = screen.getByTestId('eye-hidden')
    input = screen.getByTestId('input')
    expect(input).toHaveAttribute('type', 'password')
  })

  it('calls onChange callback when input value changes', () => {
    const mockOnChange = jest.fn()
    render(<Password onChange={mockOnChange} />)

    const input = screen.getByTestId('input')
    fireEvent.change(input, { target: { value: 'SecurePassword123!' } })

    expect(mockOnChange).toHaveBeenCalledWith('SecurePassword123!')
  })

  it('works without onChange callback', () => {
    expect(() => {
      render(<Password />)
      const input = screen.getByTestId('input')
      fireEvent.change(input, { target: { value: 'SecurePassword123!' } })
    }).not.toThrow()
  })

  it('applies correct CSS classes to input', () => {
    render(<Password />)

    const input = screen.getByTestId('input')
    expect(input).toHaveClass('text-black')
    expect(input).toHaveClass('h-[100%]')
    expect(input).toHaveClass('w-5/6')
    expect(input).toHaveClass('border-none')
  })

  it('applies correct CSS classes to eye icon', () => {
    render(<Password />)

    const eyeIcon = screen.getByTestId('eye-hidden')
    expect(eyeIcon).toHaveClass('ml-[5px]')
    expect(eyeIcon).toHaveClass('md:h-[50px]')
    expect(eyeIcon).toHaveClass('h-[25px]')
  })
})
