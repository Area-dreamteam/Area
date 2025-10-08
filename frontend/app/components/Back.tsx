/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Back
*/

'use client'

import { Button } from "@/components/ui/button"
import { useRouter } from 'next/navigation';

interface BackProps {
  dir?: string | null
}

export default function BackButton({ dir = null }: BackProps) {
  const router = useRouter();

  return (
    <Button className="rounded-full border-white hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[30px] py-[20px] text-[15px] font-bold" onClick={() => { if (!dir) router.back(); else router.push(dir) }}>
      ᐸ Back
    </Button>
  )
}
