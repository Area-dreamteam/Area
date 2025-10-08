/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { fetchPersonalApplets } from "@/app/functions/fetch";
import taskbarButton from "@/app/components/TaskBarButtons";
import { PrivateApplet } from "@/app/types/applet";
import Applets from "@/app/components/Applets";
import { Input } from "@/components/ui/input";
import { useState, useEffect } from "react";
import { redirect } from "next/navigation";

function redirectToApplet(applet: PrivateApplet)
{
    redirect(`/applets/${applet.name}`);
}

export default function My_applet()
{
    const [searched, setSearched] = useState<string>("");
    const [applets, setApplets] = useState(null);
    const [page, setPage] = useState("All");

    useEffect(() => {
        fetchPersonalApplets(setApplets);
    }, [])
    console.log(applets);

    return (
        <div className="w-screen">
            <h1 className="flex justify-center text-[50px] font-bold mt-[50px]">My Applets</h1>
            <Input className="mx-auto block w-[400px] h-[50px] mt-[20px] mb-[20px] border-[4px]" placeholder="Search Applets or Services" onChange={(e) => setSearched(e.target.value)}/>
            <div className="mx-auto block w-1/2">
                <div className="flex justify-around mb-[20px]">
                    {taskbarButton("All", page, setPage, true)}
                    {taskbarButton("Published", page, setPage, true)}
                </div>
            </div>
            <Applets search={searched} widgets={applets} className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer" onClick={redirectToApplet}/>
        </div>
    )
}