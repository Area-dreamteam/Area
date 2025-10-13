/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { useEffect } from 'react';
import { use, useState } from 'react';
import { notFound } from "next/navigation";
import { redirect } from "next/navigation";
import BackButton from '@/app/components/Back';
import { Button } from '@/components/ui/button';
import SettingsButton from '@/app/components/Settings';
import { PrivateApplet, SpecificPrivateApplet } from "@/app/types/applet";
import { fetchPrivateApplet, fetchPersonalApplets, fetchDeletePersonApplet } from '@/app/functions/fetch';

type AppletProp = {
  params: Promise<{ slug: string }>;
};

async function deleteApplet(id: number)
{
    await fetchDeletePersonApplet(id);
    redirect("/my_applets");
}

export default function AppletPage({ params }: AppletProp)
{
    const slug = decodeURIComponent(use(params).slug);
    const [loading, setLoading] = useState(true);
    const [applets, setApplets] = useState<PrivateApplet[] | null>(null);
    const [myApplet, setMyApplet] = useState<SpecificPrivateApplet | null>(null);
    const [currApplet, setCurrApplet] = useState<PrivateApplet | undefined>(undefined);

    useEffect(() => {
        const loadApplets = async () => {
            await fetchPersonalApplets(setApplets);
        }
        loadApplets();
    }, [])

    useEffect(() => {
        if (applets != null) {
            const searched = applets.find(applet => applet.name.toLowerCase() == (slug.toLowerCase()));
            setCurrApplet(searched);
            
            if (!searched)
                setLoading(false);
        }
    }, [applets]);

    useEffect(() => {
        if (currApplet)
            fetchPrivateApplet(setMyApplet, currApplet.id);
    }, [currApplet])

    useEffect(() => {
        if (myApplet != null)
            setLoading(false);
    }, [myApplet]);

    return (
        <div>
            {loading ? (
                <p className="h-[700px] w-screen text-[50px] flex items-center justify-center">
                    Loading...
                </p>
            ) : (myApplet && currApplet) ? (
                <div>
                    <div className="grid grid-cols-4 text-white w-screen h-[500px] rounded-b-xl" style={{ background: myApplet.area_info.color }}>
                    <div className="ml-[20px] pt-[50px]">
                    <BackButton/>
                    </div>
                    <div className="flex flex-col mt-[50px] text-[35px] mb-[20px] font-bold col-span-2 mx-auto">
                            <p className="text-[30px]">{myApplet.area_info.name}</p>
                            <p className="mb-[20px]">{myApplet.area_info.description}</p>
                        </div>
                        <div className="flex justify-end pt-[50px] mr-[20px]">
                            <SettingsButton link={`/my_applets/${myApplet.area_info.name}/edit`}/>
                        </div>
                    </div>
                    <Button className="mt-[25px] mb-[25px] w-[300px] h-[70px] rounded-full text-white font-semibold transition-colors duration-300 hover:cursor-pointer block mx-auto text-[25px]" onClick={() => deleteApplet(currApplet.id)}>
                        Delete applet
                    </Button>
                </div>
            ) : notFound()}
        </div>
    );
}
