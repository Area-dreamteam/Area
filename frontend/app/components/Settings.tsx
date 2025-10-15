/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Back
*/

'use client'

import redirectToPage from "../functions/redirections";
import { Button } from "@/components/ui/button";
import Link from "next/link";

interface SettingsProp
{
    link: string
}

export default function SettingsButton({link}: SettingsProp)
{
    return (
        <Button className="rounded-full border-white hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[30px] py-[20px] text-[15px] font-bold" onClick={() => redirectToPage(link)}>
            <Link href="settings">
                ⚙ Settings
            </Link>
        </Button>
    )
}