/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** register
*/
'use client'

import { RiEyeFill, RiEyeOffFill } from "react-icons/ri";
// import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { useState } from 'react';

export default function Register()
{
    const [isPasswordTyping, setIsPasswordTyping] = useState(false);

    return (
        <div className="bg-[#FFFFFF] h-screen">
            <div>
                <Link href="/" className="flex justify-center text-[100px] text-black">Area</Link>
                <h1 className="flex justify-center text-[50px] text-black mb-10">Register</h1>
                <form>
                    <div className="flex justify-center">
                        <input className="text-black h-[50px] w-[300px] mb-5 outline-4 pl-2 rounded-xl" placeholder="Email" type="email"/>
                    </div>
                    <div className="flex justify-center flex-row">
                        <input className="text-black h-[50px] w-[300px] outline-4 pl-2 mb-10  rounded-xl" placeholder="Password" type="password" onChange={(e) => {
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
                        <Button className="flex justify-center mb-3 bg-[#000000] text-white hover:text-black text-[30px] hover:bg-[#73bbff] rounded-full w-[350px] h-[100px] pt-2.5">
                            Get started
                        </Button>
                    </div>
                    <p className="flex justify-center">Or</p>
                    <div className="flex justify-center">
                        <hr className="w-[350px] outline-[1px] mb-[25px]" style={{ color: "#4400ff"}}/>
                    </div>
                    <div className="flex justify-center">
                        <Link href="" className="flex justify-center mb-3 bg-white text-black text-[30px] hover:bg-[#e4e4e4] rounded-full w-[350px] h-[100px] hover:border-[#000000] border-[#e4e4e4] border-[2px] outline-[1px] pt-[25px]">
                            Continue with Google
                        </Link>
                    </div>
                    <div className="flex justify-center mb-[25px]">
                        <Button className="flex justify-center mb-3 bg-[#4400ff] text-white hover:text-black text-[30px] hover:bg-[#73bbff] rounded-full w-[350px] h-[100px]">
                            Continue with Facebook
                        </Button>
                    </div>
                    <div className="flex justify-center">
                        <p className="mb-3 text-black text-center text-[30px] w-[350px] h-[100px]">
                            Already have an account ? <br/><Link href="/login" className="hover:text-[#4400ff] underline">Log in</Link>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    )
}