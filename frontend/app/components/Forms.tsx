/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Forms
*/

import Link from 'next/link'
import { useState } from 'react';
import { Input } from "@/components/ui/input"
import { RiEyeFill, RiEyeOffFill } from "react-icons/ri";

interface Information
{
    onChange?: Function
}

export function Mail({onChange = (() => "")} : Information)
{
    return (
        <div className="h-[50px] w-[300px] flex-row outline-[1px] rounded-xl mb-[15px]">
            <Input className="text-black h-[50px] w-[250px] ml-[10px] mb-[20px] border-none focus-visible:outline-none focus-visible:ring-0 focus-visible:border-transparent" pattern="[a-zA-Z0-9._\-]+@[a-zA-Z0-9_\-]+\.[a-z]{2,}$" placeholder="Email" type="email" onChange={(e) => onChange(e.target.value)} title="[mail]@[domain].[extension]" required/>
        </div>
    )
}

interface PasswordProps {
    w?: string,
    onChange?: Function
}

export function Password({w = "100%", onChange = (() => "")}: PasswordProps)
{
    const [isPsswdVisible, setIsPsswdVisible] = useState(false);
    const [psswdType, setPsswdType] = useState("password");

    function swapPsswdComponents()
    {
        setPsswdType(psswdType == "password" ? "text" : "password");
        setIsPsswdVisible(!isPsswdVisible);
    }

    return (
        <div className="flex justify-items h-[50px] flex-row outline-[1px] rounded-xl mb-[15px]" style={{ width: w}}>
            {isPsswdVisible && (
                <RiEyeFill className="ml-[5px] h-[50px]" onClick={() => swapPsswdComponents()}/>
            )}
            {!isPsswdVisible && (
                <RiEyeOffFill className="ml-[5px] h-[50px]" onClick={() => swapPsswdComponents()}/>
            )}
            <Input className="text-black h-[50px] w-[250px] pl-2 ml-[10px] mb-[20px] border-none focus-visible:outline-none focus-visible:ring-0 focus-visible:border-transparent" placeholder="Password" type={psswdType} onChange={(e) => onChange(e.target.value)} pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$" required/>
        </div>
    )
}
