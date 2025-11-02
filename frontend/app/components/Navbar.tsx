'use client'

import {
  NavigationMenu,
  NavigationMenuList,
} from '@/components/ui/navigation-menu'
import MenuButton from './MenuButtons'
import { Button } from '@/components/ui/button'
import Link from 'next/link'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { useRouter } from 'next/navigation'
import { fetchLogout } from '@/app/functions/fetch'

export default function NavigationBar() {
  return (
    <NavigationMenu className="flex flex-row-reverse">
      <NavigationMenuList>
        {MenuButton('Explore', '/explore')}
        {MenuButton('Download App', '/client.apk')}
        {MenuButton('Login', '/login')}
        {MenuButton('Register', '/register')}
      </NavigationMenuList>
    </NavigationMenu>
  )
}

function ProfileDropdown() {
  const router = useRouter();

  return (
    <div className="overflow-hidden rounded-full">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline">:::</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56" align="start">
          <DropdownMenuGroup>
            <DropdownMenuItem
              className="hover:cursor-pointer md:hidden"
              onClick={() => router.push('/create')}
            >
              Create
            </DropdownMenuItem>
            <DropdownMenuItem
              className="hover:cursor-pointer md:hidden"
              onClick={() => router.push('/my_applets')}
            >
              My applets
            </DropdownMenuItem>
            <DropdownMenuItem
              className="hover:cursor-pointer md:hidden"
              onClick={() => router.push('/explore')}
            >
              Explore
            </DropdownMenuItem>
            <DropdownMenuItem
              className="hover:cursor-pointer"
              onClick={() => router.push('/settings')}
            >
              Account
            </DropdownMenuItem>
            <DropdownMenuItem
              className="hover:cursor-pointer"
              onClick={() => router.push('/help')}
            >
              Help
            </DropdownMenuItem>
            <DropdownMenuItem
              className="hover:cursor-pointer"
              onClick={() => router.push('/client.apk')}
            >
              Download Mobile App
            </DropdownMenuItem>
            <DropdownMenuItem
              className="hover:cursor-pointer"
              onClick={async () => {
                await fetchLogout()
                router.push('/')
              }}
            >
              Log out
            </DropdownMenuItem>
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}

export function ConnectedNavbar() {
  return (
    <div className="flex justify-between pb-[5px] ml-[10px] mt-[10px] shadow-xl">
      <Link href="/explore" className="font-bold text-[35px]">
        {' '}
        Area{' '}
      </Link>
      <NavigationMenu className="flex flex-row-reverse border-1 rounded-xl pl-[5px]">
        {ProfileDropdown()}
        <NavigationMenuList className="hidden md:flex">
          {MenuButton('Create', '/create')}
          {MenuButton('My applets', '/my_applets')}
          {MenuButton('Explore', '/explore')}
        </NavigationMenuList>
      </NavigationMenu>
    </div>
  )
}
