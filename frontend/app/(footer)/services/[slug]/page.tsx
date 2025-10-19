/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import Image from "next/image";
import { useEffect } from 'react';
import { use, useState } from 'react';
import { notFound } from "next/navigation";
import { redirect } from "next/navigation";
import BackButton from '@/app/components/Back';
import { useAuth } from "@/app/functions/hooks";
import { Button } from '@/components/ui/button';
import { fetchServices } from '@/app/functions/fetch';
import { fetchSpecificService } from '@/app/functions/fetch';
import { Service, SpecificService } from "@/app/types/service";
import { fetchIsConnected, redirectOauthAddService } from "@/app/functions/oauth";

type ServiceProp = {
  params: Promise<{ slug: string }>;
};

export default function ServicePage({ params }: ServiceProp) {
  const { slug } = use(params);
  const [loadings, setLoading] = useState(true);
  const [services, setServices] = useState<Service[] | null>(null);
  const [myService, setMyService] = useState<SpecificService | null>(null);
  const [currService, setCurrService] = useState<Service | undefined>(undefined);
  const [serviceConnected, setserviceConnected] = useState<boolean>(false);
  const { user, loading } = useAuth();

  useEffect(() => {
    const loadServices = async () => {
      await fetchServices(setServices);
    }
    loadServices();
  }, [])


  useEffect(() => {
    if (services != null) {
      const searched = services.find(service => service.name.toLowerCase() == (slug.toLowerCase()));
      setCurrService(searched);
      if (!searched)
        setLoading(false);
    }
  }, [services]);

  useEffect(() => {
    if (currService)
      fetchSpecificService(setMyService, currService.id);
  }, [currService])

  useEffect(() => {
    if (myService != null)
      setLoading(false);
  }, [myService]);

  useEffect(() => {
    if (!myService)
      return;
    const loadServices_connected = async () => {
      await fetchIsConnected(myService.id, setserviceConnected);
    }
    loadServices_connected()
  }, [myService]);

  return (
    <form>
      {loadings ? (
        <p className="h-[700px] w-screen text-[50px] flex items-center justify-center">
          Loading...
        </p>
      ) : myService ? (
        <div>
          <div className="grid grid-cols-4 text-white w-screen h-[500px] rounded-b-xl" style={{ background: myService.color }}>
            <div className="ml-[20px] pt-[50px]">
              <BackButton dir={"/explore"} />
            </div>
            <div className="flex flex-col justify-end text-[35px] mb-[20px] font-bold col-span-2 mx-auto">
              {myService.image_url &&
                <Image alt="myService's image" src={myService.image_url} width={200} height={200} className="rounded-xl w-[250px] h-[250px]" />
              }
              <p className="mb-[20px]">{myService.description}</p>
              <p className="text-[20px]">{myService.name}</p>
            </div>
          </div>
          {serviceConnected ? (
            <Button className="mt-[25px] mb-[25px] w-[300px] h-[70px] rounded-full text-white font-semibold transition-colors duration-300 hover:cursor-pointer block mx-auto text-[25px]" onClick={() => redirect("/create")}>
              Create applet
            </Button>
          ) : user ? (
            <Button className="mt-[25px] mb-[25px] w-[300px] h-[70px] rounded-full text-white font-semibold transition-colors duration-300 hover:cursor-pointer block mx-auto text-[25px]" onClick={() => redirectOauthAddService(myService.name, user.id)}>
              Connect to {myService.name}
            </Button>
          ) : null}
        </div>
      ) : notFound()}
    </form>
  );
}
