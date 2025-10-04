/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import redirectToPage from "@/app/functions/redirections";

const elements = [
    {
        id: 1,
        title: "Account",
        linked_page: "/account",
        desc: "Area basics and managing your account"
    },
    {
        id: 2,
        title: "Applets",
        linked_page: "/applets",
        desc: "Creating, managing and troubleshooting Applets"
    },
    {
        id: 3,
        title: "Services",
        linked_page: "/services",
        desc: "Services on Area and tips on how to troubleshoot"
    },
    // {
    //     title: "Getting started guide and tutorials",
    //     linked_page: "/",
    //     desc: "Learn how to get started using Area and view tutorials covering advanced use cases."
    // },
]

export default function Help()
{
    const blocks = elements.map(elem => (
        <Button key={elem.id} onClick={() => redirectToPage(elem.linked_page)} className="w-[300px] h-[100px] bg-[#acacac]">
            <p>{elem.title}</p>
            <p>{elem.desc}</p>
        </Button>
    ));

    return (
        <div>
            <h1 className="flex justify-center mt-[150px] text-[50px] font-bold mb-[20px]">Help Center</h1>
            <h2 className="flex justify-center text-[25px] text-[#8a8a8a] mb-[20px]">Answers to frequently asked questions</h2>
            <Input className="flex justify-center w-1/2 border-[5px] h-[50px] text-[25px] mb-[20px] hover:border-[#90b8f3]" placeholder="Search"/>
            <div className="flex justify-around">
                {blocks}
            </div>
        </div>
    )
}