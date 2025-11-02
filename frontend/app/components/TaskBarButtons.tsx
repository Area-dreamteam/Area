/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** TaskBarButtons
 */

import { Button } from '@/components/ui/button'

export default function taskbarButton(
  buttonName: string,
  selected: string,
  setPage: (str: string) => void,
  enable: boolean
) {
  return (
    <Button
      aria-label={`See ${buttonName}`}
      className="bg-white hover:bg-white hover:text-[#424242] text-black font-bold text-[15px] hover:cursor-pointer"
      onClick={() => setPage(buttonName)}
      style={{ textDecoration: selected == buttonName ? 'underline' : '' }}
      disabled={!enable}
    >
      {buttonName}
    </Button>
  )
}
