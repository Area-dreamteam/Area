/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** Back
 */

'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'

interface BackProps {
  dir?: string | null
}

export default function BackButton({ dir = null }: BackProps) {
  const router = useRouter()

  return (
    <Button
      aria-label={dir ? `Go to ${dir}` : "Go to last page"}
      className="rounded-full border-white hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[20%] py-[20px] simple-text font-bold"
      onClick={(event) => {
        event.preventDefault()
        if (!dir) router.back()
        else router.push(dir)
      }}
    >
      ᐸ Back
    </Button>
  )
}
