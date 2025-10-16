/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Timestamp } from "next/dist/server/lib/cache-handlers/types"
import { fetchServices, fetchApplets } from "@/app/functions/fetch"
import taskbarButton from "@/app/components/TaskBarButtons"
import Services from "@/app/components/Services"
import { Button } from "@/components/ui/button"
import Applets from "@/app/components/Applets"
import { Service } from "@/app/types/service"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { redirect } from "next/navigation"
import {
DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuCheckboxItem,
} from "@radix-ui/react-dropdown-menu"

function customDropdown(text: string | null, disable: boolean, 
    setFilter: (str: string | null) => void, id: number)
{
    return (
        <DropdownMenuCheckboxItem key={id} className={`hover:bg-[#9ca2ff] hover:text-white pl-[5px] ${disable ? "bg-[#0084ff] text-white" : ""} rounded-md`} onClick={(e) => setFilter(text)}>
            {text ? text : "All services"}
        </DropdownMenuCheckboxItem>
    )
}

interface FilterProp
{
    filter: string | null,
    services: Service[] | null,
    setFilter: (str: string | null) => void
}

function Filter({services, filter, setFilter}: FilterProp)
{
    const dropdownTitles = (services? services.map(service => service.category) : ""); // to ensure there's no doublons. Need to complete by searching how to get doubles off
    const dropdownFilters = (services? services.map(service => {
        return (
            customDropdown(service.category, filter == service.category, setFilter, service.id)
        )
    }
    ) : "");

    return (
        <div className="flex justify-center">
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button className="ring-[2px] ring-black bg-white text-black text-[15px] hover:bg-white font-bold">
                        {filter ? filter : "All services"}
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="bg-white rounded-md border-1 pl-[5px] pr-[5px]">
                <DropdownMenuLabel className="font-bold pb-[10px]">
                    Filters
                </DropdownMenuLabel>
                {customDropdown(null, filter == null, setFilter, -1)}
                <DropdownMenuLabel className="font-bold pb-[10px]">
                    Categories
                </DropdownMenuLabel>
                {dropdownFilters}
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    )
}

interface Applet {
    id: number,
    name: string,
    description: string,
    user: {
      id: number,
      name: string
    },
    enable: boolean,
    created_at: Timestamp,
    color: string
}

interface SearchProp {
    search?: string
    services?: Service[] | null
    applets?: Applet[] | null
}

function All({search = "", services = null, applets = null}: SearchProp)
{
    return (
        <div>
            <h1 className="flex justify-center font-bold text-[25px]"> Services </h1>
            <Services search={search} services={services} className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer border-black border-[2px]" onClick={redirectToService}/>
            <br/>
            <h1 className="flex justify-center font-bold text-[25px]"> Applets </h1>
            <Applets search={search} applets={applets}  className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer border-black border-[2px]" onClick={redirectToApplet}/>
        </div>
    )
}

function redirectToService(service: Service)
{
    redirect(`/services/${service.name}`);
}

function redirectToApplet(applet: Applet)
{
    redirect(`/applets/${applet.name}`);
}

export default function Explore()
{
    const [page, setPage] = useState("All");
    const [searched, setSearched] = useState("");
    const [filter, setFilter] = useState<string | null>(null);
    const [applets, setApplets] = useState<Applet[] | null>(null);
    const [services, setServices] = useState<Service[] | null>(null);

    useEffect(() => {
        fetchServices(setServices);
        fetchApplets(setApplets);
    }, [])

    return (
        <div>
            <h1 className="font-bold text-[100px] flex justify-center"> Explore </h1>
            <div className="flex justify-center">
                <div className="flex justify-around w-1/2">
                    {taskbarButton("All", page, setPage, true)}
                    {taskbarButton("Applets", page, setPage, true)}
                    {taskbarButton("Services", page, setPage, true)}
                </div>
            </div>
            <br/>
            <Input className="mx-auto block w-[400px]" placeholder="Search Applets or Services" onChange={(e) => setSearched(e.target.value)}/>
            <br/>
            {page == "Services"  && <Filter services={services} filter={filter} setFilter={setFilter}/>}
            <div className="flex justify-center">
                <div>
                    {page == "Services" && <Services filter={filter} search={searched} services={services} className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer border-black border-[2px]" onClick={redirectToService}/>}
                    {page == "Applets" && <Applets search={searched} applets={applets}  className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer" onClick={redirectToApplet}/>}
                </div>
                {page == "All" && <All search={searched} services={services} applets={applets}/>}
            </div>
        </div>
    )
}
