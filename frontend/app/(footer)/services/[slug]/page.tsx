/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** page
 */

'use client'

import Image from 'next/image'
import { useEffect } from 'react'
import { use, useState } from 'react'
import { notFound, useRouter } from 'next/navigation'
import BackButton from '@/app/components/Back'
import { useAuth } from '@/app/functions/hooks'
import { fetchSpecificService } from '@/app/functions/fetch'
import { Service, SpecificService } from '@/app/types/service'
import { redirectOauthAddService } from '@/app/functions/oauth'
import {
  fetchIsConnected,
  fetchServices,
  fetchDisconnectService,
} from '@/app/functions/fetch'
import { getImageUrl } from '@/app/functions/images'
import Markdown from '@/app/components/Markdown'

type ServiceProp = {
  params: Promise<{ slug: string }>
}

async function disconnectOauth(
  id: number,
  setReload: (arg: boolean) => void,
  reload: boolean
) {
  await fetchDisconnectService(id)
  setReload(!reload)
}

export default function ServicePage({ params }: ServiceProp) {
  const slug = decodeURIComponent(use(params).slug)
  const [reload, setReload] = useState<boolean>(false)
  const [loadings, setLoading] = useState<boolean>(true)
  const [services, setServices] = useState<Service[] | null>(null)
  const [myService, setMyService] = useState<SpecificService | null>(null)
  const [currService, setCurrService] = useState<Service | undefined>(undefined)
  const [serviceConnected, setserviceConnected] = useState<boolean>(false)
  const { user } = useAuth()
  const router = useRouter();

  useEffect(() => {
    const loadServices = async () => {
      await fetchServices(setServices)
    }
    loadServices()
  }, [])

  useEffect(() => {
    if (services != null) {
      const searched = services.find(
        (service) => service.name.toLowerCase() == slug.toLowerCase()
      )
      setCurrService(searched)
      if (!searched) setLoading(false)
    }
  }, [services])

  useEffect(() => {
    if (currService) fetchSpecificService(setMyService, currService.id)
  }, [currService])

  useEffect(() => {
    if (!myService) return
    const loadServices_connected = async () => {
      await fetchIsConnected(myService.id, setserviceConnected)
    }
    loadServices_connected()
    window.addEventListener('message', (event) => {
      if (event.data.type === `${myService.name}_login_complete`) {
        setserviceConnected(true)
      }
    })
  }, [myService, reload])

  useEffect(() => {
    if (myService != null) setLoading(false)
  }, [myService])

  return (
    <div>
      {loadings ? (
        <p className="h-[700px] w-screen text-[50px] flex items-center justify-center">
          Loading...
        </p>
      ) : myService ? (
        <div>
          <div
            className="grid grid-cols-4 text-white w-screen h-[500px] rounded-b-xl"
            style={{ background: myService.color }}
          >
            <div className="ml-[20px] pt-[50px]">
              <BackButton dir={'/explore'} />
            </div>
            <div className="col-span-2 flex flex-col items-center justify-center text-[35px] font-bold text-center">
              {myService.image_url && getImageUrl(myService.image_url) != "" && (
                <Image
                  alt="myService's image"
                  src={getImageUrl(myService.image_url)}
                  width={150}
                  height={150}
                  className="rounded-xl m-4"
                />
              )}
              <div className="mb-[20px]">
                <Markdown>{myService.description}</Markdown>
              </div>
              <p className="text-[20px]">{myService.name}</p>
            </div>
          </div>
          {!myService.oauth_required ? (
            <button
              aria-label="This button redirects you to the applet's creation page"
              className="mt-[25px] mb-[25px] rounded-button inverted block mx-auto"
              onClick={(e) => {
                e.preventDefault()
                router.push('/create')
              }}
            >
              Create applet
            </button>
          ) : !serviceConnected && myService.oauth_required && user ? (
            <button
              className="mt-[25px] mb-[25px] rounded-button inverted block mx-auto"
              onClick={() =>
                redirectOauthAddService(myService.name, user.id, null)
              }
            >
              Connect to {myService.name}
            </button>
          ) : serviceConnected && myService.oauth_required && user ? (
            <button
              className="mt-[25px] mb-[25px] rounded-button inverted block mx-auto"
              onClick={() => disconnectOauth(myService.id, setReload, reload)}
            >
              Disconnect to {myService.name}
            </button>
          ) : null}
        </div>
      ) : (
        notFound()
      )}
    </div>
  )
}
