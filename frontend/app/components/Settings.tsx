/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** Back
 */

'use client'

import { Button } from '@/components/ui/button'
import Link from 'next/link'
import { redirect, useRouter } from 'next/navigation'

interface SettingsProp {
  link: string
}

export default function SettingsButton({ link }: SettingsProp) {
  const router = useRouter();

  return (
    <Button
      className="rounded-full border-white hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[10%] py-[20px] simple-text font-bold"
      onClick={(e) => {
        e.preventDefault()
        router.push(link);
      }}
    >
      <Link href="settings">⚙ Settings</Link>
    </Button>
  )
}
