/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** MenuButtons
 */

'use client'

import Link from 'next/link'
import {
  NavigationMenuItem,
  NavigationMenuLink,
} from '@/components/ui/navigation-menu'
import { redirect, useRouter } from 'next/navigation'

export default function MenuButton(text: string, linkedPage: string) {
  const router = useRouter();

  return (
    <NavigationMenuItem>
      <NavigationMenuLink
        asChild
        className="text-1 p-3 w-[15vw] h-10 hover:text-[#4400ff] centered bg-transparent"
        style={{ fontFamily: 'Open Sans' }}
        onClick={(e) => {
          e.preventDefault();
          router.push(linkedPage);
        }}
      >
        <Link href={linkedPage} className="text-center">
          {text}
        </Link>
      </NavigationMenuLink>
    </NavigationMenuItem>
  )
}
