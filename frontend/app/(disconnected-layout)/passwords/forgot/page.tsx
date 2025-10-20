/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Link from "next/link"

export default function forgotPassword()
{
    return (
        <div>
            <h1 className="centered text-[50px] text-black mb-10 font-bold mt-[50px]">Forgot your password ?</h1>
            <div className="centered">
                <Input type="email" className="text-black h-[50px] w-[500px] pl-2 mb-[20px] border-[4px] rounded-xl placeholder:text-[20px] placeholder:font-bold" placeholder="Your email address"></Input>
            </div>
                <p className="centered text-[20px] mb-[30px]">
                    We will send you a link to reset your password.
                </p>
                <div className="centered">
                    <Button className="mb-3 bg-[#000000] text-white text-[40px] hover:bg-[#383838] rounded-full w-[350px] h-[100px] pt-2.5 font-bold">
                        <Link href="/login">
                            Reset password
                        </Link>
                    </Button>
                </div>
        </div>
    )
}