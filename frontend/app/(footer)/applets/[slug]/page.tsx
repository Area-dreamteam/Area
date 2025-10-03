/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { notFound } from 'next/navigation';
import appletsData from '@/data/applets.json';
import BackButton from '@/app/components/Back';
import SettingsButton from '@/app/components/Settings';
import { Applet, AppletsFormat } from "@/types/applet";
import { Button } from '@/components/ui/button';
import { use } from 'react';

type AppletProp = {
  params: Promise<{ slug: string }>;
};

const applets: AppletsFormat = appletsData;

export default function AppletPage({ params }: AppletProp) {
    const { slug } = use(params);
    const applet: Applet | undefined = applets[slug]
    
    if (!applet)
        return notFound();

    return (
        <form>
            <div className="grid grid-cols-4 text-white w-screen h-[500px] rounded-b-xl" style={{ background: applet.color }}>
                <div className="ml-[20px] pt-[50px]">
                    <BackButton/>
                </div>
                <div className="flex flex-col justify-end text-[35px] mb-[20px] font-bold col-span-2 mx-auto">
                    <p className="mb-[20px]">{applet.description}</p>
                    <p className="text-[20px]">{applet.name}</p>
                    <p className="text-[20px]">{applet.created_at}</p>
                </div>
                <div className="flex justify-end pt-[50px] mr-[20px]">
                    <SettingsButton/>
                </div>
            </div>
            <Button className={`mt-[25px] mb-[25px] w-[300px] h-[70px] rounded-full text-white font-semibold transition-colors duration-300 hover:cursor-pointer block mx-auto text-[25px] ${applet.activated ? 'bg-red-400 hover:bg-red-600' : 'bg-green-400 hover:bg-green-600'}`} onClick={() => applet.activated = !applet.activated}>
                {applet.activated ? "Disconnect" : "Connect"}
            </Button>

        </form>
    );
}
