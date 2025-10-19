/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Input } from "@/components/ui/input";
import { useEffect, use, useState } from "react";
import ValidateButton from "@/app/components/Validation";
import { PrivateApplet, SpecificPrivateApplet } from "@/app/types/applet";
import { fetchPrivateApplet, fetchPersonalApplets } from '@/app/functions/fetch';
import redirectToPage from "@/app/functions/redirections";

type AppletProp = {
    params: Promise<{ slug: string }>;
};

function editApplet(appletName: string)
{
    redirectToPage(`/my_applets/${appletName}`);
}

function modifyApplet()
{
    
}

export default function Edit({ params }: AppletProp)
{
    const slug = decodeURIComponent(use(params).slug);
    const [loading, setLoading] = useState(true);
    const [applets, setApplets] = useState<PrivateApplet[] | null>(null);
    const [myApplet, setMyApplet] = useState<SpecificPrivateApplet | null>(null);
    const [currApplet, setCurrApplet] = useState<PrivateApplet | undefined>(undefined);
    const [modifiedApplet, setModifiedApplet] = useState<SpecificPrivateApplet | null>(null);

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
        if (myApplet != null) {
            setLoading(false);
            setModifiedApplet(myApplet);
        }
    }, [myApplet]);

    return (
        <div style={{ background: myApplet?.area_info.color}}>
            {loading ?  (
                ""
               ) : (
                (myApplet && modifiedApplet &&
                    <div className="mx-[50px] py-[50px]">
                        <h1 className="centered text-[40px] font-bold">
                            {myApplet?.area_info.name}
                        </h1>
                        <hr className="mt-[25px] mb-[25px]"/>
                        <p>
                            Created by: {myApplet.area_info.user.name}<br/>
                            At: {new Date(myApplet.area_info.created_at).toLocaleDateString()}
                        </p>
                        <Input className="bg-white text-black w-[600px]" defaultValue={myApplet.area_info.description ? myApplet.area_info.description : ""} placeholder="description"/>
                        <Input className="bg-white text-black w-[600px]" defaultValue={myApplet.area_info.color} placeholder="color" onChange={() => modifyApplet()}/>
                        <br/>
                        <ValidateButton clickAct={() => editApplet(modifiedApplet.area_info.name)} arg={true} text="Validate" addToClass="mt-[50px]"/>
                    </div>
                )
            )}
        </div>
    )
}
