/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { use } from 'react';
import Image from "next/image";
import { notFound } from 'next/navigation';
import BackButton from '@/app/components/Back';
import servicesData from '@/data/services.json';
import { Button } from '@/components/ui/button';
import SettingsButton from '@/app/components/Settings';
import { Service, ServicesFormat } from "@/types/service";

type AppletProp = {
  params: Promise<{ slug: string }>;
};

const services: ServicesFormat = servicesData;

export default function AppletPage({ params }: AppletProp) {
    const { slug } = use(params);
    const service: Service | undefined = services[slug]
    
    if (!service)
        return notFound();

    return (
        <form>
            <div className="grid grid-cols-4 text-white w-screen h-[500px] rounded-b-xl" style={{ background: service.color }}>
                <div className="ml-[20px] pt-[50px]">
                    <BackButton/>
                </div>
                <div className="flex flex-col justify-end text-[35px] mb-[20px] font-bold col-span-2 mx-auto">
                    <Image alt="service's logo" src={service.logo} width={4000} height={4000} className="rounded-xl w-[250px] h-[250px]"/>
                    <p className="mb-[20px]">{service.desc}</p>
                    <p className="text-[20px]">{service.name}</p>
                </div>
                <div className="flex justify-end pt-[50px] mr-[20px]">
                    <SettingsButton/>
                </div>
            </div>
            <Button className="mt-[25px] mb-[25px] w-[300px] h-[70px] rounded-full text-white font-semibold transition-colors duration-300 hover:cursor-pointer block mx-auto text-[25px]" disabled>
                Create applet
            </Button>

        </form>
    );
}
