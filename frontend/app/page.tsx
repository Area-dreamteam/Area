/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

import Link from "next/link"

function RecommandedApplets()
{
  return (
    <div>

    </div>
  )
  // I'll put the applats later, now i'm focusing on the login and register
}

export default function Home()
{
  return (
    <div className="bg-[#FFFFFF] h-screen font-bold">
      <div className="bg-[#000000] h-5/7">
        <h1 className="text-white text-[50px]">Area</h1>
        <h1 className="flex text-white justify-center text-center text-[90px] pt-[70px]">Automation for business and home</h1>
        <h2 className="flex text-white justify-center text-[25px]">Build your own chain of reactions</h2>
        <div className="flex justify-center mt-20">
          <Link href="/register" className="bg-[#FFFFFF] pt-[25px] text-center text-[#000000] hover:bg-[#73bbff] rounded-full w-[300px] h-[100px] text-4xl">
            Start now
          </Link>
        </div>
      </div>
      <div className="">
        <h3 className="flex justify-center mt-[75px] text-black text-[35px] font-bold">Get started with any Applet</h3>
        <RecommandedApplets/>
      </div>
    </div>
  );
}
