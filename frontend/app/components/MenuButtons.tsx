/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** MenuButtons
*/

'use client'

import {
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu"
import Link from "next/link"
import { redirect } from "next/navigation"

export default function MenuButton(text: string, linkedPage: string)
{
  return (
    <NavigationMenuItem>
      <NavigationMenuLink asChild className="text-1 p-3 w-[15vw] h-10 hover:text-[#4400ff] flex justify-center bg-transparent" style={{ fontFamily: "Open Sans" }} onClick={() => redirect(linkedPage)}>
        <Link href={linkedPage} className="text-center">
          {text}
        </Link>
      </NavigationMenuLink>
    </NavigationMenuItem>
  )
}
