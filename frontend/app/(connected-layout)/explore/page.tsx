/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Timestamp } from "next/dist/server/lib/cache-handlers/types"
import { fetchServices, fetchApplets } from "@/app/functions/fetch"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react" 
import { Service } from "@/app/types/service"
import Image from "next/image"
import Link from "next/link"
import {
DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuCheckboxItem,
} from "@radix-ui/react-dropdown-menu"

function taskbarButton(buttonName: string, selected: string,
    setPage: (str: string) => void, enable: boolean)
{
    return (
        <Button className="bg-white hover:bg-white hover:text-[#424242] text-black font-bold text-[15px]" onClick={() => setPage(buttonName)} style={{ textDecoration: (selected == buttonName ? "underline" : "") }} disabled={!enable}>
            {buttonName}
        </Button>
    )
}

function customDropdown(text: string)
{
    return (
        <DropdownMenuCheckboxItem className="hover:bg-[#a5c1e5] pl-[5px] rounded-md">
            {text}
        </DropdownMenuCheckboxItem>
    )
}

function Filter()
{
    return (
        <div className="flex justify-center">
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button className="ring-[2px] ring-black bg-white text-black text-[15px] hover:bg-white font-bold">
                        All services
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="bg-white rounded-md border-1 pl-[5px] pr-[5px]">
                <DropdownMenuLabel className="font-bold pb-[10px]">Filters</DropdownMenuLabel>
                {customDropdown("All services")}
                {customDropdown("New services")}
                {customDropdown("Popular services")}
                <DropdownMenuLabel className="font-bold pb-[1px]">Categories</DropdownMenuLabel>
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

function Services({search = "", services = null}: SearchProp)
{
    if (services == null)
        return (
            <p className="flex justify-center text-[20px] mt-[20px]">
                No service found.
            </p>
        )
    const filteredServices = services.filter(service =>
        service.name.toLowerCase().includes(search.toLowerCase())
    );
    const nbServices = filteredServices.length;
    const serviceBlocks = services.map((service) => ((
        service.name.toLowerCase().includes(search.toLowerCase()) ?
        (
            <Link href={`/services/${service.name}`} key={service.id} className="rounded-xl w-[250px] h-[300px]" style={{ backgroundColor: service.color }}>
                { service.logo == "" || service.logo == null ? "" : (<Image alt="service's logo" src={service.logo} width={200} height={200} className="rounded-xl w-[250px] h-[250px]"/>)}
                <div className="flex justify-center">
                    <p className="font-bold text-white text-[20px] m-[20px]">{service.name}</p>
                </div>
            </Link>
        ) : (
            ""
        )
    )))

    return (
        <div>
            {nbServices != 0 ? (
                <div className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center">
                    {serviceBlocks} 
                </div>
            ) : (
                <p className="flex justify-center text-[20px] mt-[20px]">
                    No service found.
                </p>
            )}
        </div>
    )
}

function Applets({search = "", applets = null}: SearchProp)
{
    if (applets == null)
        return (
            <p className="flex justify-center text-[20px] mt-[20px]">
                No applet found.
            </p>
        )
    const filteredApplets = applets.filter(applet =>
        applet.name.toLowerCase().includes(search.toLowerCase())
    );
    const nbApplets = filteredApplets.length;
    const appletBlocks = Object.values(applets).map((applet) => (
        applet.name.toLowerCase().includes(search.toLowerCase()) ?
        (
            <Link href={`/applets/${applet.name}`} key={applet.id} className="rounded-xl w-[250px] h-[300px]" style={{ backgroundColor: applet.color }}>
                <div className="flex justify-center">
                    <p className="font-bold text-white text-[20px] m-[20px]">{applet.name}</p>
                </div>
            </Link>
        ) : (
        ""
    )))

    return (
        <div>
            {nbApplets != 0 ? (
                <div className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center">
                {appletBlocks}
            </div>
            ) : (
                <p className="flex justify-center text-[20px] mt-[20px]">
                    No applet found.
                </p>
            )}
        </div>
    )
}

function All({search = "", services = null, applets = null}: SearchProp)
{
    return (
        <div>
            <h1 className="flex justify-center font-bold text-[25px]"> Services </h1>
            <Services search={search} services={services}/>
            <br/>
            <h1 className="flex justify-center font-bold text-[25px]"> Applets </h1>
            <Applets search={search} applets={applets}/>
        </div>
    )
}

export default function Explore()
{
    const [page, setPage] = useState("All");
    const [searched, setSearched] = useState("");
    const [services, setServices] = useState(null);
    const [applets, setApplets] = useState(null);

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
            <div className="flex justify-center">
                <Input className="w-[400px]" placeholder="Search Applets or Services" onChange={(e) => setSearched(e.target.value)}/>
            </div>
            <br/>
            {page == "Services"  && <Filter/>}
            <div className="flex justify-center">
                {page == "Services" && <Services search={searched} services={services}/>}
                {page == "Applets" && <Applets search={searched} applets={applets}/>}
                {page == "All" && <All search={searched} services={services} applets={applets}/>}
            </div>
        </div>
    )
}