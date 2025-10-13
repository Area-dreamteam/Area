/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** register
*/

'use client'

import { Password, Mail } from "../components/Forms"
import { fetchRegister } from "../functions/fetch"
import { AlertCircleIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useRouter } from 'next/navigation'
import { useState } from "react"
import Link from "next/link"
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
import { redirectOauth } from "../functions/oauth"

export default function Register() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [error, setError] = useState(false);
  const [password, setPassword] = useState("");

  async function sendRegisterForm(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const success: boolean = await fetchRegister(email, password);

    if (success)
      router.push("/login");
    else
      setError(true);
  }

  return (
    <div className="bg-[#FFFFFF] h-screen font-bold">
      <div>
        <Link href="/" className="flex justify-center text-[100px] text-black hover:text-[#424242]">Area</Link>
        <h1 className="flex justify-center text-[50px] text-black mb-10">Register</h1>
        <form onSubmit={(e) => sendRegisterForm(e)}>
          <div className="flex justify-center">
            <Mail onChange={setEmail} />
          </div>
          <div className="flex justify-center">
            <Password w={"300px"} onChange={setPassword} />
          </div>
          {error &&
            <Alert variant="destructive" className="bg-red-100 rounded-4xl mb-[20px] mr-[20px] w-[300px] mx-auto">
              <AlertCircleIcon />
              <AlertTitle>Sorry, this account already exist.</AlertTitle>
            </Alert>
          }
          <div className="flex justify-center">
            <Button className="flex justify-center mb-3 bg-[#000000] text-white hover:text-black text-[40px] hover:bg-[#73bbff] rounded-full w-[350px] h-[100px] font-bold pt-2.5 hover:cursor-pointer" type="submit">
              Get started
            </Button>
          </div >
        </form>
      </div>
      <p className="flex justify-center">Or</p>
      <div className="flex justify-center">
        <hr className="w-[350px] outline-[1px] mb-[25px]" style={{ color: "#4400ff" }} />
      </div>
      <div className="flex justify-center">
        <Button onClick={() => redirectOauth("github")} className="flex justify-center mb-[20px] bg-white text-black text-[30px] hover:bg-[#e4e4e4] rounded-full w-[450px] h-[70px] hover:border-[#000000] border-[#e4e4e4] border-[2px] outline-[1px] pt-[10px]">
          Continue with Github
        </Button>
      </div>
      <div className="flex justify-center">
        <p className="mb-3 text-black text-center text-[20px]">
          Already have an account ? <Link href="/login" className="hover:text-[#4400ff] underline">Log in here.</Link>
        </p>
      </div>
    </div>
  )
}
