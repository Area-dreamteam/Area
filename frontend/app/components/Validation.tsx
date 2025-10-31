/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** Validation
 */

interface ValidationProp {
  arg: boolean
  text: string
  center?: boolean
  addToClass?: string
  inverted?: boolean
  clickAct: (status: boolean) => void
}

export default function ValidateButton({
  addToClass = '',
  arg,
  text,
  center = true,
  clickAct,
  inverted = false,
}: ValidationProp) {
  return (
    <button
      className={`rounded-button ${center ? 'mx-auto block' : ''} ${addToClass} ${inverted ? 'inverted' : ''} ${addToClass}`}
      onClick={() => clickAct(arg)}
    >
      {text}
    </button>
  )
}
