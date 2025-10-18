/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Forms
*/

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
        <div className="logins-container">
            <Input
            className="text-black h-[100%] w-5/6 border-none focus-visible:ring-0 md:placeholder:text-sm placeholder:text-xs md:text-sm text-xs"
            pattern="[a-zA-Z0-9._\-]+@[a-zA-Z0-9_\-]+\.[a-z]{2,}$"
            placeholder="Email" type="email"
            onChange={(e) => onChange(e.target.value)}
            title="[mail]@[domain].[extension]" required/>
        </div>
    )
}

interface PasswordProps {
    w?: string,
    onChange?: Function
}

export function Password({onChange = (() => "")}: PasswordProps)
{
    const [isPsswdVisible, setIsPsswdVisible] = useState(false);
    const [psswdType, setPsswdType] = useState("password");

    function swapPsswdComponents()
    {
        setPsswdType(psswdType == "password" ? "text" : "password");
        setIsPsswdVisible(!isPsswdVisible);
    }

    return (
        <div className="flex justify-items logins-container">
            {isPsswdVisible && (
                <RiEyeFill className="ml-[5px] md:h-[50px] h-[25px]" onClick={() => swapPsswdComponents()}/>
            )}
            {!isPsswdVisible && (
                <RiEyeOffFill className="ml-[5px] md:h-[50px] h-[25px]" onClick={() => swapPsswdComponents()}/>
            )}
            <Input
            className="text-black h-[100%] w-5/6 border-none focus-visible:ring-0 md:placeholder:text-sm placeholder:text-xs md:text-sm text-xs"
            placeholder="Password"
            type={psswdType}
            onChange={(e) => onChange(e.target.value)}
            pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$" required/>
        </div>
    )
}
