/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** layout
*/
import { ConnectedNavbar } from "../components/Navbar"
import Link from "next/link"

function Footer() {
  return (
    <div className="bg-black text-white w-full font-bold pl-[10px] bottom-0">
      <Link href="/explore" className="mt-[50px] text-[50px]">Area</Link>
      <div className="grid grid-cols-3 pb-[25px]">
        <div className="flex flex-col mt-[10px] gap-[10px] text-[20px]">
          <Link href="/explore">Explore</Link>
          <Link href="/services">Services</Link>
          <Link href="/applets">Applets</Link>
          <Link href="/help">Help center</Link>
        </div>
      </div>
      <p className="pb-[25px] centered"> This website has been made by Boris Cheng, Idriss Dupoisot, Gauthier Fagot, Luc Simon and Léo Barbier</p>
    </div>
  )
}

export default function ExploreLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div>
      <ConnectedNavbar/>
      {children}
      <Footer/>
    </div>
  );
}

