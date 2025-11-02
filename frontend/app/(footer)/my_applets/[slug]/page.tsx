/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { useEffect } from 'react'
import { use, useState } from 'react'
import { notFound, useRouter, useSearchParams } from 'next/navigation'
import BackButton from '@/app/components/Back'
import SettingsButton from '@/app/components/Settings'
import {
  PrivateApplet,
  PublicApplet,
  SpecificPrivateApplet,
  SpecificPublicApplet,
} from '@/app/types/applet'
import {
  fetchPersonalApplets,
  fetchDeletePersonalApplet,
  fetchPersonalAppletConnection,
  fetchPublishPersonalApplet,
  fetchPrivateApplet,
  fetchUnpublishPersonalApplet,
  fetchPersonalPublicApplets,
  fetchSpecificApplet,
} from '@/app/functions/fetch'
import Markdown from '@/app/components/Markdown'

type AppletProp = {
  params: Promise<{ slug: string }>
}

async function deleteApplet(id: number) {
  await fetchDeletePersonalApplet(id)
}

async function AppletConnection(
  id: number,
  state: string,
  setConnectionChanged: (arg: boolean) => void
) {
  await fetchPersonalAppletConnection(id, state)
  setConnectionChanged(true)
}

async function UnpublishApplet(id: number) {
  await fetchUnpublishPersonalApplet(id)
}

async function publishApplet(id: number) {
  await fetchPublishPersonalApplet(id)
}

export default function AppletPage({ params }: AppletProp) {
  const slug = use(params).slug;
  const searchParams = useSearchParams()
  const [loading, setLoading] = useState(true)
  const published = searchParams.get('published') === 'true'
  const [applets, setApplets] = useState<
    PublicApplet[] | PrivateApplet[] | null
  >(null)
  const [areaChanged, setAreaChanged] = useState<boolean>(false)
  const [currApplet, setCurrApplet] = useState<
    PublicApplet | PrivateApplet | undefined
  >(undefined)
  const [myApplet, setMyApplet] = useState<
    SpecificPublicApplet | SpecificPrivateApplet | null
  >(null)
  const router = useRouter();

  useEffect(() => {
    const loadApplets = async () => {
      await (published
        ? fetchPersonalPublicApplets(setApplets)
        : fetchPersonalApplets(setApplets))
    }
    loadApplets()
  }, [])

  useEffect(() => {
    if (applets != null) {
      const searched = applets.find(
        (applet) => applet.id == Number(slug)
      )
      setCurrApplet(searched)
      if (!searched) {
        setLoading(false)
      }
    }
  }, [applets]);

  useEffect(() => {
    const getSpecificApplet = async () => {
      if (currApplet) {
        await (published 
          ? fetchSpecificApplet(setMyApplet, currApplet.id)
          : fetchPrivateApplet(setMyApplet, currApplet.id))
        setLoading(false)
      }
    }
    getSpecificApplet();
  }, [currApplet, published])

  useEffect(() => {
    if (!areaChanged) return
    if (currApplet) {
      if (published) {
        fetchSpecificApplet(setMyApplet, currApplet.id)
      } else {
        fetchPrivateApplet(setMyApplet, currApplet.id)
      }
    }
    setAreaChanged(false)
  }, [areaChanged, currApplet])

  return (
    <div>
      {loading ? (
        <p className="h-[700px] w-screen text-[50px] flex items-center justify-center">
          Loading...
        </p>
      ) : myApplet ? (
        <div className="w-screen h-max">
          <div
            className={`grid grid-cols-4 text-white ${published ? 'h-max' : 'rounded-b-xl md:h-[500px] h-[300px]'}`}
            style={{ background: myApplet.area_info.color }}
          >
            <div className="ml-[20px] pt-[50px]">
              <BackButton dir={'/my_applets'} />
            </div>
            <div className="flex flex-col mt-[50px] text-[35px] mb-[20px] font-bold col-span-2 mx-auto w-[100%]">
              <p className="text-center simple-text inverted truncate">
                {myApplet.area_info.name}
              </p>
              <div className="text-center simple-text inverted line-clamp-3">
                <Markdown>{myApplet.area_info.description}</Markdown>
              </div>
              {published ? (
                <button
                  aria-label="Click here to unpublish your applet"
                  className="md:my-[150px] my-[100px] little-rounded-button centered lg:w-[40%] w-[60%]"
                  onClick={() => { UnpublishApplet(myApplet.area_info.id); router.push("/my_applets") }}
                >
                  Unpublish
                </button>
              ) : (
                <button
                  aria-label={`Click here to ${(myApplet as SpecificPrivateApplet).area_info.enable ? 'disable' : 'enable'} your applet`}
                  className="md:my-[100px] my-[50px] little-rounded-button centered lg:w-[40%] w-[60%]"
                  onClick={() => {
                    const privApplet = myApplet as SpecificPrivateApplet
                    AppletConnection(
                      privApplet.area_info.id,
                      privApplet.area_info.enable ? 'disable' : 'enable',
                      setAreaChanged
                    )
                  }}
                >
                  {(myApplet as SpecificPrivateApplet).area_info.enable
                    ? 'Disconnect'
                    : 'Connect'}
                </button>
              )}
            </div>
            <div className="flex justify-end pt-[50px] mr-[20px]">
              <SettingsButton
                link={`/my_applets/${myApplet.area_info.id}/edit`}
              />
            </div>
          </div>
          {!published && (
            <div className="grid grid-cols-2">
              <button
                className="w-[50%] mt-[25px] mb-[25px] block mx-auto rounded-button inverted [--common-bg:#BA301C] [--common-hover:#801100]"
                onClick={() => { deleteApplet(myApplet.area_info.id); router.push('/my_applets'); }}
              >
                Delete applet
              </button>
              <button
                aria-label={`Click on this button if you want to make your applet public so everyone can copy it`}
                className="w-[50%] mt-[25px] mb-[25px] block mx-auto rounded-button inverted"
                onClick={() => publishApplet(myApplet.area_info.id)}
              >
                Publish
              </button>
            </div>
          )}
        </div>
      ) : (
        notFound()
      )}
    </div>
  )
}
