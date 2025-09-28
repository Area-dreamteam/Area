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
        name: "instagram",
        desc: "no caption yet",
        color: "#85bcf9",
        logo: "https://upload.wikimedia.org/wikipedia/fr/7/75/Snapchat.png?20230424210458"
    },
    {
        id: "8794",
        user_id: "046576",
        name: "Snapchat",
        desc: "stupid invention",
        color: "#dbda82",
        logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/960px-Instagram_icon.png"
    }
]

export default function Explore()
{
    const [page, setPage] = useState("All");
    const blocks = services.map((service) => (
        <div key={service.id} className="flex items-end rounded-xl w-[250px] h-[300px]" style={{ backgroundColor: service.color }}>
            <p className="font-bold text-white text-[20px] m-[20px]">{service.name}</p>
            {/* <Image alt="service's logo" src={service.logo} width={100} height={100}/> */}
        </div>
    ))

    return (
        <div>
            <h1 className="font-bold text-[100px] flex justify-center"> Explore </h1>
            <div className="flex justify-center">
                <div className="flex justify-around w-1/2">
                    <Button className="bg-white hover:bg-white hover:text-[#424242] text-black font-bold text-[15px]" onClick={() => setPage("All")}>All</Button>
                    <Button className="bg-white hover:bg-white hover:text-[#424242] text-black font-bold text-[15px]" onClick={() => setPage("Applets")}>Applets</Button>
                    <Button className="bg-white hover:bg-white hover:text-[#424242] text-black font-bold text-[15px]" onClick={() => setPage("Services")}>Services</Button>
                    <Button className="bg-white hover:bg-white hover:text-[#424242] text-black font-bold text-[15px]" onClick={() => setPage("Stories")}>Stories</Button>
                </div>
            </div>
            <br/>
            <div className="flex justify-center">
                <Input className="w-[400px]" placeholder="Search Apllets or Services"/>
            </div>
            <br/>
            <div className="flex justify-center">
                <DropdownMenu>
                    <DropdownMenuTrigger >
                        All services
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                    <DropdownMenuLabel className="font-bold pb-[10px]">Filters</DropdownMenuLabel>
                    <DropdownMenuCheckboxItem>All services</DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem>New services</DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem>Popular services</DropdownMenuCheckboxItem>
                    <DropdownMenuLabel className="font-bold pb-[1px]">Categories</DropdownMenuLabel>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
            <div className="mt-[50px] flex justify-around">
                {blocks}
            </div>
        </div>
    )
}