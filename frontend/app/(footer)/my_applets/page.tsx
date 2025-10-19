/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { fetchPersonalApplets } from "@/app/functions/fetch";
import taskbarButton from "@/app/components/TaskBarButtons";
import { PrivateApplet, PublicApplet } from "@/app/types/applet";
import Applets from "@/app/components/Applets";
import { Input } from "@/components/ui/input";
import { useState, useEffect } from "react";
import { redirect } from "next/navigation";

function redirectToApplet(applet: PublicApplet | PrivateApplet)
{
    redirect(`/my_applets/${applet.name}`);
}

function FilterApplets(text: string, applets: PrivateApplet[] | null)
{
    if (applets === null)
        return applets;
    if (text === "Enabled") {
        const filteredApplets = applets.filter(applet => (
            applet.enable
        ))
        return filteredApplets;
    }
    if (text === "Published") {
        const filteredApplets = applets.filter(() => (
            false // to modify when variable published will be added
        ))
        return filteredApplets;
    }
    return applets;
}

export default function My_applet()
{
    const [applets, setApplets] = useState<PrivateApplet[] | null>(null);
    const [searched, setSearched] = useState<string>("");
    const [page, setPage] = useState("All");

    useEffect(() => {
        fetchPersonalApplets(setApplets);
    }, [])

    return (
        <div className="w-screen">
            <h1 className="centered text-[50px] font-bold mt-[50px]">My Applets</h1>
            <Input className="mx-auto block w-[400px] h-[50px] mt-[20px] mb-[20px] border-[4px]" placeholder="Search Applets or Services" onChange={(e) => setSearched(e.target.value)}/>
            <div className="mx-auto block w-1/2">
                <div className="flex justify-around mb-[20px]">
                    {taskbarButton("All", page, setPage, true)}
                    {taskbarButton("Published", page, setPage, true)}
                    {taskbarButton("Enabled", page, setPage, true)}
                </div>
            </div>
            <Applets search={searched} applets={FilterApplets(page, applets)} className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer mb-[20px] border-black border-[2px]" onClick={redirectToApplet}/>
        </div>
    )
}