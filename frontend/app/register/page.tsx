/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** register
*/

'use client'

import facebook from "@/public/images/Facebook_logo.png"
import { Password, Mail } from "../components/Forms"
import { fetchRegister } from "../functions/fetch"
import { Button } from "@/components/ui/button"
import { redirect } from 'next/navigation'
import { useState } from "react"
import Image from "next/image"
import Link from "next/link"


export default function Register()
{
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    async function sendForm()
    {
        const success : boolean = await fetchRegister(email, password);

        if (success)
            redirect("/login");
    }

    return (
        <div className="bg-[#FFFFFF] h-screen font-bold">
            <div>
                <Link href="/" className="flex justify-center text-[100px] text-black hover:text-[#424242]">Area</Link>
                <h1 className="flex justify-center text-[50px] text-black mb-10">Register</h1>
                <form onSubmit={sendForm}>
                    <div className="flex justify-center">
                        <Mail onChange={setEmail}/>
                    </div>
                    <div className="flex justify-center">
                        <Password w={"300px"} onChange={setPassword}/>
                    </div>
                    <div className="flex justify-center">
                        <Button className="flex justify-center mb-3 bg-[#000000] text-white hover:text-black text-[40px] hover:bg-[#73bbff] rounded-full w-[350px] h-[100px] pt-2.5 hover:cursor-pointer" type="submit">
                            Get started
                        </Button>
                    </div>
                    <p className="flex justify-center">Or</p>
                    <div className="flex justify-center">
                        <hr className="w-[350px] outline-[1px] mb-[25px]" style={{ color: "#4400ff"}}/>
                    </div>
                    <div className="flex justify-center">
                        <Link href="https://google.com" className="flex justify-center mb-[20px] bg-white text-black text-[30px] hover:bg-[#e4e4e4] rounded-full w-[450px] h-[70px] hover:border-[#000000] border-[#e4e4e4] border-[2px] outline-[1px] pt-[10px]">
                            Continue with Google
                        </Link>
                    </div>
                    <div className="flex justify-center">
                        <Link href="https://apple.com" className="flex justify-center mb-[20px] bg-black text-white text-[30px] hover:bg-[#3a3a3a] rounded-full w-[450px] h-[70px] hover:border-[#000000] border-[#e4e4e4] border-[2px] outline-[1px] pt-[10px]">
                            Continue with Apple
                        </Link>
                    </div>
                    <div className="flex justify-center">
                        <Link href="https://google.com" className="flex justify-center mb-[20px] bg-black text-white text-[30px] hover:bg-[#3a3a3a] rounded-full w-[450px] h-[70px]  border-[2px] pt-[10px] pl-[25px] pr-[25px]">
                            <Image alt="Facebook logo" src={facebook} sizes="100vw" style={{ width: '30px', height: '30px', marginRight: "25px" }}/>
                            Continue with Facebook
                        </Link>
                    </div>
                    <div className="flex justify-center">
                        <p className="mb-3 text-black text-center text-[20px]">
                            Already have an account ? <Link href="/login" className="hover:text-[#4400ff] underline">Log in here.</Link>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    )
}
