/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** login
*/

'use client'

import { RiEyeFill, RiEyeOffFill } from "react-icons/ri";
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Image from "next/image"
import Link from "next/link"
import { useState } from 'react';
import facebook from "@/public/images/Facebook_logo.png"
import { redirect } from 'next/navigation'

export default function Register()
{
    const [isPsswdVisible, setIsPsswdVisible] = useState(false);
    const [psswdType, setPsswdType] = useState("password");

    function swapPsswdComponents()
    {
        setPsswdType(psswdType == "password" ? "text" : "password");
        setIsPsswdVisible(!isPsswdVisible);
    }

    return (
        <div className="bg-[#FFFFFF] h-screen font-bold">
            <div>
                <Link href="/" className="flex justify-center text-[100px] text-black hover:text-[#424242]">Area</Link>
                <h1 className="flex justify-center text-[50px] text-black mb-10">Log in</h1>
                <form>
                    <div className="flex justify-center">
                        <div className="h-[50px] w-[300px] flex-row outline-[1px] rounded-xl mb-[15px]">
                            <Input className="text-black h-[50px] w-[250px] ml-[10px] mb-[20px] border-none focus-visible:outline-none focus-visible:ring-0 focus-visible:border-transparent" placeholder="Email" type="email"/>
                        </div>
                    </div>
                    <div className="flex justify-center">
                        <div className="flex justify-center h-[50px] w-[300px] flex-row outline-[1px] rounded-xl mb-[15px]">
                            {isPsswdVisible && (
                                <RiEyeFill className="ml-[5px] h-[50px]" onClick={() => swapPsswdComponents()}/>
                                )}
                            {!isPsswdVisible && (
                                <RiEyeOffFill className="ml-[5px] h-[50px]" onClick={() => swapPsswdComponents()}/>
                                )}
                            <Input className="text-black h-[50px] w-[250px] pl-2 ml-[10px] mb-[20px] border-none focus-visible:outline-none focus-visible:ring-0 focus-visible:border-transparent" placeholder="Password" type={psswdType}/>
                        </div>
                    </div>
                    <div className="flex justify-center">
                        <Link href="/passwords/forgot" className="flex justify-center mb-[30px] text-black text-center text-[20px] hover:text-[#676767] underline">
                            Forgot your password ?
                        </Link>
                    </div>
                    <div className="flex justify-center">
                        <Button className="flex justify-center mb-3 bg-[#000000] text-white text-[40px] hover:bg-[#383838] rounded-full w-[350px] h-[100px] pt-2.5 font-bold">
                            <Link href="/explore">
                                Log in
                            </Link>
                        </Button>
                    </div>
                    <p className="flex justify-center">Or</p>
                    <div className="flex justify-center">
                        <hr className="w-[350px] outline-[1px] mb-[30px]" style={{ color: "#4400ff"}}/>
                    </div>
                    <div className="flex justify-center">
                        <Link href="https://google.com" className="flex justify-center mb-[20px] bg-white text-black text-[30px] hover:bg-[#e4e4e4] rounded-full w-[450px] h-[70px] hover:border-[#000000] border-[#e4e4e4] border-[2px] outline-[1px] pt-[10px]">
                            Continue with Google
                        </Link>
                    </div>
                    <div className="flex justify-center">
                        <Link href="https://google.com" className="flex justify-center mb-[20px] bg-black text-white text-[30px] hover:bg-[#3a3a3a] rounded-full w-[450px] h-[70px]  border-[2px] pt-[10px] pl-[25px] pr-[25px]">
                        <Image alt="Facebook logo" src={facebook} sizes="100vw" style={{ width: '30px', height: '30px', marginRight: "25px" }}/>
                        Continue with Facebook
                        </Link>
                    </div>
                    <p className="flex justify-center mb-3 text-black text-center text-[20px]">
                        New to Area ? <Link href="/register" className="hover:text-[#4400ff] underline">Sign up here.</Link>
                    </p>
                </form>
            </div>
        </div>
    )
}