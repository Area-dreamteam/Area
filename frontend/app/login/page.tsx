/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** login
*/

'use client'

import { RiEyeFill, RiEyeOffFill } from "react-icons/ri";
// import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { useState } from 'react';

export default function Login()
{
    const [isPasswordTyping, setIsPasswordTyping] = useState(false);

    return (
        <div className="bg-[#FFFFFF] h-screen">
            <div>
                <h1 className="flex justify-center text-[100px] text-black">Area</h1>
                <h1 className="flex justify-center text-[50px] text-black mb-10">Login</h1>
                <form>
                    <div className="flex justify-center">
                        <input className="flex justify-center text-black mb-5 outline-2 pl-2 rounded-m" placeholder="Email" type="email"/>
                    </div>
                    <div className="flex justify-center flex-row">
                        <input className="text-black outline-2 pl-2 mb-10  rounded-m" placeholder="Password" type="password" onChange={(e) => {
                            setIsPasswordTyping(e.target.value.length > 0);
                        }}
                        />
                        {/* {isPasswordTyping && (
                            <RiEyeOffFill/>
                        )}
                        {!isPasswordTyping && (
                            <RiEyeFill/>
                        )} */}
                    </div>
                    <div className="flex justify-center">
                        <Button className="flex justify-center mb-3 bg-[#4400ff] text-white hover:text-black text-[30px] hover:bg-[#77bbff] rounded-xl w-[350px] h-[100px] pt-2.5">
                            Log to your account
                        </Button>
                    </div>
                    <div className="flex justify-center">
                        <Link href="/register" className="flex justify-center pt-6 mb-3 bg-[#4400ff] text-white hover:text-black text-[30px] hover:bg-[#77bbff] rounded-xl w-[350px] h-[100px]">
                            No account ? Register
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    )
}