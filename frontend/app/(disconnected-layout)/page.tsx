/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** page
 */

'use client'

import { useEffect, useState } from 'react'
import { fetchApplets } from '../functions/fetch'
import { PublicApplet } from '../types/applet'
import { useRouter } from 'next/navigation'

function RecommandedApplets()
{
  const router = useRouter();
  const [applets, setApplets] = useState<
    (PublicApplet)[] | null
  >(null)

  useEffect(() => {
    fetchApplets(setApplets)
  }, [])

  if (applets == null) {
    return "";
  }
  const nbServices = applets.length
  const serviceBlocks = applets.map((applet) =>
    <div
      key={applet.id}
      className="rounded-xl w-[250px] h-[300px] hover:cursor-pointer"
      style={{ backgroundColor: applet.color }}
      onClick={() => router.push(`/applets/${applet.id}`)}
    >
      <div className="centered bg-black rounded-t-lg">
        <p className="font-bold text-white text-[20px] m-[20px]">
          {applet.name}
        </p>
      </div>
    </div>
  )

  return (
    <div className="w-full">
      <h3 className="mt-[5%] subtitle centered text-black">
        Get started with any Applet
      </h3>
      {nbServices != 0 ? (
        <div className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 justify-items-center">{serviceBlocks.slice(0, 3)}</div>
      ) : (
        <p className="centered text-[20px] mt-[20px]">Please connect yourself to see available applets.</p>
      )}
    </div>
  )
}

export default function Home()
{
  const router = useRouter();

  return (
    <div className="font-bold">
      <div className="bg-black rounded-b-2xl">
        <h1
          onClick={(e) => {
            e.preventDefault()
            router.push('/explore')
          }}
          className="logo inverted w-0"
        >
          Area
        </h1>
        <h1 className="title inverted centered">
          Automation for business and home
        </h1>
        <h2 className="subtitle centered">Build your own chain of reactions</h2>
        <div className="centered mt-[10%]">
          <button
            aria-label="Click here to register or login to Area"
            onClick={(e) => {
              e.preventDefault()
              router.push('/register')
            }}
            className="rounded-button m-[5%]"
          >
            Start now
          </button>
        </div>
      </div>
      <RecommandedApplets/>
      <br/>
    </div>
  )
}