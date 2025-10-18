/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Button } from "@/components/ui/button";
import redirectToPage from "../functions/redirections";

function RecommandedApplets()
{
  return (
    <div>

    </div>
  )
  // I'll put the applets later, now i'm focusing on the login and register
}

export default function Home()
{
  return (
    <div className="font-bold">
      <div className="bg-black rounded-b-2xl">
        <h1 onClick={() => redirectToPage("/explore")} className="logo inverted">
          Area
        </h1>
        <h1 className="title inverted centered">
          Automation for business and home
        </h1>
        <h2 className="subtitle centered">
          Build your own chain of reactions
        </h2>
        <div className="centered mt-[10%]">
          <button onClick={() => redirectToPage("/register")} className="rounded-button m-[5%]">
            Start now
          </button>
        </div>
      </div>
      <h3 className="mt-[5%] title-part text-black">
        Get started with any Applet
      </h3>
      <RecommandedApplets/>
    </div>
  );
}
