/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Password } from "@/app/components/Forms"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function changePassword()
{
    return (
        <div className="mx-auto mt-[40px] w-[700px] font-bold">
            <h1 className="flex justify-center text-[50px] mt-[40px] font-bold">
                Change password
            </h1>
            <hr/>
            <br/>
            <h3 className="text-[20px]">
                Username
            </h3>
            <p className="text-gray-400 text-[20px] mb-[20px]">Pseudo</p>
            <h3 className="text-[20px] mb-[5px]">
                Current password
            </h3>
            <Password/>
            <Link href="/passwords/forgot" className="text-[#0099ff] text-center text-[20px] hover:text-[#676767]">
                Forgot your password ?
            </Link>
            <br/><br/>
            <h3 className="text-[20px] mb-[5px]">
                New password
            </h3>
            <Password/>
            <br/>
            <h3 className="text-[20px] mb-[5px]">
                Confirm new password
            </h3>
            <Password/>
            <Button className="block mx-auto text-[40px] mt-[70px] text-white w-[300px] h-[100px] rounded-full font-bold mb-[20px]" disabled>
                Change
            </Button>
            <Link href="/settings" className="flex justify-center text-[20px] underline">Cancel</Link>
        </div>
    )
}