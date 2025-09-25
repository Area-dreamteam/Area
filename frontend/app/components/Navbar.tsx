/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Navbar
*/

import Link from "next/link"
import {
    Menubar,
    MenubarContent,
    MenubarItem,
    MenubarMenu,
    MenubarSeparator,
    MenubarShortcut,
    MenubarTrigger,
} from "@/components/ui/menubar"

function MenuButton(string: string, linkedPage: string)
{
  return (
    <MenubarTrigger className="text-1 p-3 w-[15vw] h-10 hover:text-[#4400ff] flex justify-center" style={{ fontFamily: "Open Sans" }}>
      <Link href={linkedPage}>
        {string}
      </Link>
    </MenubarTrigger>
  )
}

export default function NavigationBar()
{
  return (
    <Menubar className="flex flex-row-reverse">
        <MenubarMenu>
            {MenuButton("Explore", "explore")}
            {MenuButton("Login", "login")}
            {MenuButton("Register", "register")}
        </MenubarMenu>
    </Menubar>
  );
}
