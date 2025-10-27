/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Input } from "@/components/ui/input";
import { useEffect, use, useState, ChangeEvent } from "react";
import ValidateButton from "@/app/components/Validation";
import { PrivateApplet, SpecificPrivateApplet } from "@/app/types/applet";
import { fetchPrivateApplet, fetchPersonalApplets, fetchUpdatePersonalApplets } from '@/app/functions/fetch';
import { notFound, redirect } from "next/navigation";

type AppletProp = {
    params: Promise<{ slug: string }>;
};

export function Warning(title: string, message: string) {
    return (
      <div className="bg-yellow-100 border border-yellow-400 text-yellow-800 px-4 py-3 rounded relative">
        {title && <strong className="font-bold">{title}: </strong>}
        <span className="block sm:inline">{message}</span>
      </div>
    );
  }
async function editApplet(title: string, desc: string, oldApplet: SpecificPrivateApplet)
{
    if (title == "" || desc == "")
        return false;
    console.log(title, desc);
    await fetchUpdatePersonalApplets(title, desc, oldApplet);
    redirect(`/my_applets/${title}`);
}

export default function Edit({ params }: AppletProp)
{
    const slug = decodeURIComponent(use(params).slug);
    const [loading, setLoading] = useState(true);
    const [applets, setApplets] = useState<PrivateApplet[] | null>(null);
    const [myApplet, setMyApplet] = useState<SpecificPrivateApplet | null>(null);
    const [currApplet, setCurrApplet] = useState<PrivateApplet | undefined>(undefined);
    const [title, setTitle] = useState<string>("");
    const [desc, setDesc] = useState<string>("");
    
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
            setTitle(myApplet.area_info.name);
            setDesc(myApplet.area_info.description);
        }
    }, [myApplet]);

    return (
        <div style={{ background: myApplet?.area_info.color}}>
            {loading ?  (
                ""
               ) : (
                (myApplet &&
                    <div className="py-[50px] h-screen w-[75%] mx-auto">
                        <Input className="centered subtitle inverted" defaultValue={myApplet.area_info.name} placeholder="Title" onChange={(e) => setTitle(e.target.value)}/>
                        <hr className="mt-[25px] mb-[25px]"/>
                        <textarea className="rounded-md bg-white text-black w-[75%] h-[20%] px-[1%] mx-auto block" defaultValue={myApplet.area_info.description ? myApplet.area_info.description : ""} placeholder="description" minLength={1} onChange={(e) => setDesc(e.target.value)} required/>
                        <br/>
                        <p className="simple-text inverted w-[75%] block mx-auto">
                            Created by: {myApplet.area_info.user.name}<br/>
                            At: {new Date(myApplet.area_info.created_at).toLocaleDateString()}
                        </p>
                        <br/>
                        <ValidateButton clickAct={() => {
                            if (!editApplet(title, desc, myApplet))
                                return Warning("Update impossible", "");
                        }} arg={true} text="Validate" addToClass="mt-[50px]"/>
                    </div>
                )
            )}
            {(!currApplet || !myApplet) && !loading &&
                notFound()
            }
        </div>
    )
}
