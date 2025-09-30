/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuCheckboxItem,
} from "@radix-ui/react-dropdown-menu"
import { useState } from "react"
import Image from "next/image"

const services = [
    {
        id: "5896",
        user_id: "0454226",
        name: "Discord",
        desc: "no caption yet",
        color: "#85bcf9",
        logo: "/images/Discord_icon.png"
    },
    {
        id: "8794",
        user_id: "046576",
        name: "Snapchat",
        desc: "stupid invention",
        color: "#FFFC00",
        logo: "/images/Snapchat_icon.png"
    },
    {
        id: "3221",
        user_id: "0454226",
        name: "Instagram",
        desc: "no caption yet",
        color: "#880729",
        logo: "/images/Instagram_icon.webp"
    }
]

const applets = [
    {
        id: 2,
        name: "example_name",
        description: "example description",
        user_id: 45,
        created_at: "ajd",
        color: "#486aef"
    },
    {
        id: 3,
        name: "Spotify",
        description: "This is a music application",
        user: {
            name: "Gauthier"
        },
        created_at: "22-05-2001",
        color: "#794694"
    },
    {
        id: 4,
        name: "Spotify",
        description: "This is a music application",
        user: {
            name: "Gauthier"
        },
        created_at: "22-05-2001",
        color: "#11e59f"
    }
]

const stories = [
    {
    }
]

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
                    <Button className="ring-[2px] ring-black bg-white text-black text-[15px] hover:bg-white font-bold">All services</Button>
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

function Services()
{
    const serviceBlocks = services.map((service) => (
        <div key={service.id} className="rounded-xl w-[250px] h-[300px]" style={{ backgroundColor: service.color }}>
            <Image alt="service's logo" src={service.logo} width={4000} height={4000} className="rounded-xl w-[250px] h-[250px]"/>
            <div className="flex justify-center">
                <p className="font-bold text-white text-[20px] m-[20px]">{service.name}</p>
            </div>
        </div>
    ))

    return (
        <div className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center">
            {serviceBlocks}
        </div>
    )
}

function Applets()
{
    const appletBlocks = applets.map((applet) => (
        <div key={applet.id} className="rounded-xl w-[250px] h-[300px]" style={{ backgroundColor: applet.color }}>
            <div className="flex justify-center">
                <p className="font-bold text-white text-[20px] m-[20px]">{applet.name}</p>
            </div>
        </div>
    ))

    return (
        <div className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center">
            {appletBlocks}
        </div>
    )
}

function All()
{
    return (
        <div>
            <h1 className="flex justify-center font-bold text-[25px]"> Services </h1>
            <Services/>
            <br/>
            <h1 className="flex justify-center font-bold text-[25px]"> Applets </h1>
            <Applets/>
        </div>
    )
}

export default function Explore()
{
    const [page, setPage] = useState("All");

    return (
        <div>
            <h1 className="font-bold text-[100px] flex justify-center"> Explore </h1>
            <div className="flex justify-center">
                <div className="flex justify-around w-1/2">
                    {taskbarButton("All", page, setPage, true)}
                    {taskbarButton("Applets", page, setPage, true)}
                    {taskbarButton("Services", page, setPage, true)}
                    {taskbarButton("Stories", page, setPage, false)}
                </div>
            </div>
            <br/>
            <div className="flex justify-center">
                <Input className="w-[400px]" placeholder="Search Apllets or Services"/>
            </div>
            <br/>
            {page == "Services"  && <Filter/>}
            <div className="flex justify-center">
                {page == "Services" && <Services/>}
                {page == "Applets" && <Applets/>}
                {page == "All" && <All/>}
            </div>
        </div>
    )
}