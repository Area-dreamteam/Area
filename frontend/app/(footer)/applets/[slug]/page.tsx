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
import { fetchApplets } from '@/app/functions/fetch';
import SettingsButton from '@/app/components/Settings';
import { fetchSpecificApplet } from '@/app/functions/fetch';
import { PublicApplet, SpecificPublicApplet } from "@/app/types/applet";

type AppletProp = {
  params: Promise<{ slug: string }>;
};

export default function AppletPage({ params }: AppletProp) {
    const { slug } = use(params);
    const [loading, setLoading] = useState(true);
    const [applets, setApplets] = useState<PublicApplet[] | null>(null);
    const [myApplet, setMyApplet] = useState<SpecificPublicApplet | null>(null);
    const [currApplet, setCurrApplet] = useState<PublicApplet | undefined>(undefined);

    useEffect(() => {
        const loadApplets = async () => {
            await fetchApplets(setApplets);
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
            fetchSpecificApplet(setMyApplet, currApplet.id);
    }, [currApplet])

    useEffect(() => {
        if (myApplet != null)
            setLoading(false);
    }, [myApplet]);

    return (
        <form>
            {loading ? (
                <p className="h-[700px] w-screen text-[50px] flex items-center justify-center">
                    Loading...
                </p>
            ) : myApplet ? (
                <div>
                    <div className="grid grid-cols-4 text-white w-screen h-[500px] rounded-b-xl" style={{ background: myApplet.area_info.color }}>
                    <div className="ml-[20px] pt-[50px]">
                    <BackButton/>
                    </div>
                    <div className="flex flex-col justify-end text-[35px] mb-[20px] font-bold col-span-2 mx-auto">
                            <p className="mb-[20px]">{myApplet.area_info.description}</p>
                            <p className="text-[20px]">{myApplet.area_info.name}</p>
                        </div>
                        <div className="flex justify-end pt-[50px] mr-[20px]">
                            <SettingsButton/>
                        </div>
                    </div>
                    <Button className="mt-[25px] mb-[25px] w-[300px] h-[70px] rounded-full text-white font-semibold transition-colors duration-300 hover:cursor-pointer block mx-auto text-[25px]" onClick={() => redirect("/create")}>
                        Create applet
                    </Button>
                </div>
            ) : notFound()}
        </form>
    );
}
