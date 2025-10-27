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
import SettingsButton from '@/app/components/Settings';
import { PrivateApplet, SpecificPrivateApplet } from "@/app/types/applet";
import { fetchPersonalApplets, fetchDeletePersonalApplet, fetchPersonalAppletConnection, fetchPublishPersonalApplet, fetchUnpublishPersonalApplet, fetchPrivateApplet } from '@/app/functions/fetch';

type AppletProp = {
  params: Promise<{ slug: string }>;
};

async function deleteApplet(id: number)
{
    await fetchDeletePersonalApplet(id);
    redirect("/my_applets");
}

async function AppletConnection(id: number, state: string,
    setConnectionChanged: (arg: boolean) => void)
{
    await fetchPersonalAppletConnection(id, state);
    setConnectionChanged(true);
}

function publishApplet(id: number)
{
    fetchPublishPersonalApplet(id);
}

export default function AppletPage({ params }: AppletProp)
{
    const slug = decodeURIComponent(use(params).slug);
    const [loading, setLoading] = useState(true);
    const [applets, setApplets] = useState<PrivateApplet[] | null>(null);
    const [connectionChanged, setAreaChanged] = useState<boolean>(false);
    const [currApplet, setCurrApplet] = useState<PrivateApplet | undefined>(undefined);
    const [myApplet, setMyApplet] = useState<SpecificPrivateApplet | null>(null);

    useEffect(() => {
        const loadApplets = async () => {
            await fetchPersonalApplets(setApplets);
        }
        loadApplets();
    }, []);

    useEffect(() => {
        if (applets != null) {
            const searched = applets.find(applet => applet.name.toLowerCase() == (slug.toLowerCase()));
            setCurrApplet(searched);
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

    useEffect(() => {
        if (!connectionChanged)
            return;
        if (currApplet)
            fetchPrivateApplet(setMyApplet, currApplet.id);
        setAreaChanged(false);
    }, [connectionChanged]);

    return (
        <div>
            {loading ? (
                <p className="h-[700px] w-screen text-[50px] flex items-center justify-center">
                    Loading...
                </p>
            ) : (myApplet) ? (
                <div className="w-screen">
                    <div className="grid grid-cols-4 text-white md:h-[500px] h-[300px] rounded-b-xl" style={{ background: myApplet.area_info.color }}>
                        <div className="ml-[20px] pt-[50px]">
                            <BackButton dir={"/my_applets"}/>
                        </div>
                        <div className="flex flex-col mt-[50px] text-[35px] mb-[20px] font-bold col-span-2 mx-auto w-[100%]">
                            <p className="text-center simple-text inverted truncate">
                                {myApplet.area_info.name}
                            </p>
                            <p className="text-center simple-text inverted truncate">
                                {myApplet.area_info.description}
                            </p>
                            <button className="my-[35%] little-rounded-button centered w-[60%]" onClick={() => AppletConnection(myApplet.area_info.id, (myApplet.area_info.enable ? "disable" : "enable"), setAreaChanged)}>
                                {myApplet.area_info.enable ? "Disconnect" : "Connect"}
                            </button>
                        </div>
                        <div className="flex justify-end pt-[50px] mr-[20px]">
                            <SettingsButton link={`/my_applets/${myApplet.area_info.name}/edit`}/>
                        </div>
                    </div>
                    <div className='grid grid-cols-2'>
                        <button className="w-[50%] mt-[25px] mb-[25px] block mx-auto rounded-button inverted [--common-bg:#BA301C] [--common-hover:#801100]" onClick={() => deleteApplet(myApplet.area_info.id)}>
                            Delete applet
                        </button>
                        <button className="w-[50%] mt-[25px] mb-[25px] block mx-auto rounded-button inverted" onClick={() => publishApplet(myApplet.area_info.id)}>
                            Publish
                        </button>
                    </div>
                </div>
            ) : notFound()}
        </div>
    );
}
