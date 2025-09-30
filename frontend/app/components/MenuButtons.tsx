/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** MenuButtons
*/

import {
    // Menubar,
    // MenubarContent,
    // MenubarItem,
    // MenubarMenu,
    // MenubarSeparator,
    // MenubarShortcut,
    MenubarTrigger,
} from "@/components/ui/menubar"
import Link from "next/link"

export default function MenuButton(text: string, linkedPage: string)
{
  return (
    <MenubarTrigger className="text-1 p-3 w-[15vw] h-10 hover:text-[#4400ff] flex justify-center" style={{ fontFamily: "Open Sans" }}>
        <Link href={linkedPage}>
            {text}
        </Link>
    </MenubarTrigger>
  )
}
