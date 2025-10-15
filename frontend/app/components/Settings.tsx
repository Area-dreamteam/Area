/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Back
*/

'use client'

import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function SettingsButton()
{
    return (
        <Button className="rounded-full border-white hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[30px] py-[20px] text-[15px] font-bold" disabled>
            <Link href="settings">
                ⚙ Settings
            </Link>
        </Button>
    )
}