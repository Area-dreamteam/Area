/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Navbar
*/

import {
    Menubar,
    MenubarMenu,
} from "@/components/ui/menubar"
import Image from "next/image";
import MenuButton from "./MenuButtons"
import { Button } from "@/components/ui/button"
import profile from "../../public/images/Profile.jpg"
import Link from "next/link"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"


export default function NavigationBar()
{
  return (
    <Menubar className="flex flex-row-reverse">
      <MenubarMenu>
        {MenuButton("Explore", "/explore")}
        {MenuButton("Login", "/login")}
        {MenuButton("Register", "/register")}
      </MenubarMenu>
    </Menubar>
  );
}

function ProfileDropdown()
{
  return (
    <div className="overflow-hidden rounded-full">
      {/* <Image alt="Profile picture" src={profile}/> */}
      <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline">:::</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="start">
        <DropdownMenuGroup>
          <DropdownMenuItem>
          <Link href="/settings">Account</Link>
            <DropdownMenuShortcut>User#84395</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            Refer a friend
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            Billing
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            My services
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            Activity
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            Archive
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            Plans
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <Link href="/help">Help</Link>
          </DropdownMenuItem>
          <DropdownMenuItem>
            <Link href="/">Log out</Link>
          </DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>
    </div>
  )
}

export function ConnectedNavbar()
{
  return (
    <div className="flex justify-between ml-[10px] mt-[10px]">
      <Link href="/explore" className="font-bold text-[35px]"> Area </Link>
    <Menubar className="flex flex-row-reverse">
      <MenubarMenu >
        {ProfileDropdown()}
        {MenuButton("Create", "/create")}
        {MenuButton("My applets", "/my_applets")}
        {MenuButton("Explore", "/explore")}
      </MenubarMenu>
    </Menubar>
    </div>
  );
}