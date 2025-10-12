/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useEffect, use, useState } from "react";
import ValidateButton from "@/app/components/Validation";
import { PrivateApplet, SpecificPublicApplet } from "@/app/types/applet";
import { fetchPrivateApplet, fetchPersonalApplets, fetchDeletePersonApplet } from '@/app/functions/fetch';
import redirectToPage from "@/app/functions/redirections";

type AppletProp = {
    params: Promise<{ slug: string }>;
};

function editApplet(appletName: string)
{
    redirectToPage(`/my_applets/${appletName}`);
}

export default function Edit({ params }: AppletProp)
{
    const slug = decodeURIComponent(use(params).slug);
    const [loading, setLoading] = useState(true);
    const [modifiedApplet, setModifiedApplet] = useState(null);
    const [applets, setApplets] = useState<PrivateApplet[] | null>(null);
    const [myApplet, setMyApplet] = useState<SpecificPublicApplet | null>(null);
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
        <div style={{ background: myApplet?.area_info.color}}>
            {loading ?  (
                ""
               ) : (
                (myApplet !== null &&
                    <div className="mx-[50px] py-[50px]">
                        <h1 className="flex justify-center text-[40px] font-bold">
                            {myApplet?.area_info.name}
                        </h1>
                        <hr className="mt-[25px] mb-[25px]"/>
                        <p>
                            Created by: {myApplet.area_info.user.name}<br/>
                            At: {new Date(myApplet.area_info.created_at).toLocaleDateString()}
                        </p>
                        <Input className="bg-white text-black w-[600px]" defaultValue={myApplet.area_info.description ? myApplet.area_info.description : ""} placeholder="description"/>
                        <Input className="bg-white text-black w-[600px]" defaultValue={myApplet.area_info.color} placeholder="color"/>
                        <br/>
                        <ValidateButton clickAct={() => editApplet(myApplet.area_info.name)} arg={modifiedApplet} text="Validate" addToClass="mt-[50px]"/>
                    </div>
                )
            )}
        </div>
    )
}
