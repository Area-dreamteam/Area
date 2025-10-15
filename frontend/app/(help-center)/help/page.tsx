/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Input } from "@/components/ui/input";
import redirectToPage from "@/app/functions/redirections";

export default function Help()
{
    return (
        <div>
            <p className="hover:cursor-pointer text-[40px]  font-bold hover:text-[#3b3b3b]" onClick={() => redirectToPage("/explore")}>Area</p>
            <h1 className="flex justify-center mt-[150px] text-[50px] font-bold mb-[20px]">Help Center</h1>
            <h2 className="flex justify-center text-[25px] text-[#8a8a8a] mb-[20px]">Answers to frequently asked questions</h2>
            <Input className="flex justify-center w-1/2 border-[5px] h-[50px] text-[25px] mb-[20px] hover:border-[#90b8f3] mx-auto" placeholder="Search"/>
            <div className="flex justify-around">
                We are sorry but no help is available for now :{"("}
            </div>
        </div>
    )
}