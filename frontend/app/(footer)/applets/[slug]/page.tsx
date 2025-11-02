/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** page
 */

'use client'

import { useEffect } from 'react'
import { use, useState } from 'react'
import { notFound } from 'next/navigation'
import BackButton from '@/app/components/Back'
import { PublicApplet, SpecificPublicApplet } from '@/app/types/applet'
import {
  fetchApplets,
  fetchSpecificApplet,
  fetchCopyApplet,
} from '@/app/functions/fetch'
import Markdown from '@/app/components/Markdown'

type AppletProp = {
  params: Promise<{ slug: string }>
}

async function copyApplet(id: number) {
  await fetchCopyApplet(id)
}

export default function AppletPage({ params }: AppletProp) {
  const slug = use(params).slug;
  const [loading, setLoading] = useState(true);
  const [applets, setApplets] = useState<
    PublicApplet[] | null
  >(null)
  const [areaChanged, setAreaChanged] = useState<boolean>(false)
  const [currApplet, setCurrApplet] = useState<
    PublicApplet | undefined
  >(undefined)
  const [applet, setMyApplet] = useState<
    SpecificPublicApplet | null
  >(null)

  useEffect(() => {
    fetchApplets(setApplets)
  }, [])

  useEffect(() => {
    if (applets != null) {
      const searched = applets.find(
        (applet) => applet.id == Number(slug)
      )
      setCurrApplet(searched)
    }
  }, [applets, slug])

  useEffect(() => {
    if (currApplet) fetchSpecificApplet(setMyApplet, currApplet.id)
  }, [currApplet])

  useEffect(() => {
    if (applet != null) setLoading(false)
  }, [applet])

  useEffect(() => {
    if (!areaChanged) return;
    if (currApplet) {
      fetchSpecificApplet(setMyApplet, currApplet.id)
    }
    setAreaChanged(false)
  }, [areaChanged, currApplet]);

  return (
    <div>
      {loading ? (
        <p className="h-[700px] w-screen text-[50px] flex items-center justify-center">
          Loading...
        </p>
      ) : applet ? (
        <div className="w-screen">
          <div
            className="grid grid-cols-4 text-white h-max"
            style={{ background: applet.area_info.color }}
          >
            <div className="ml-[20px] pt-[50px]">
              <BackButton dir={'/my_applets'} />
            </div>
            <div className="flex flex-col mt-[50px] text-[35px] mb-[20px] font-bold col-span-2 mx-auto w-[100%]">
              <p className="text-center simple-text inverted truncate">
                {applet.area_info.name}
              </p>
              <div className="text-center simple-text inverted line-clamp-3">
                <Markdown>{applet.area_info.description}</Markdown>
              </div>
              <button
                aria-label={`This button allow you to copy the applet named ${applet.area_info.name}`}
                className="md:my-[150px] my-[100px] little-rounded-button centered lg:w-[40%] w-[60%]"
                onClick={() => copyApplet(applet.area_info.id)}
              >
                Copy
              </button>
            </div>
            <div className="flex justify-end pt-[50px] mr-[20px]">
            </div>
          </div>
        </div>
      ) : (
        notFound()
      )}
    </div>
  )
}
