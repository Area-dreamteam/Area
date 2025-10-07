/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** login
*/

'use client'

import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
import Link from "next/link"
import Image from "next/image"
import { useEffect, useState } from "react"
import { useRouter } from 'next/navigation'
import { AlertCircleIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { fetchLogin } from "../functions/fetch"
import { Password, Mail } from "../components/Forms"
import facebook from "@/public/images/Facebook_logo.png"
import { redirectOauthGithub, redirectOauthTodoist } from "../functions/oauth"

export default function Login() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [error, setError] = useState(false);
  const [password, setPassword] = useState("");

  async function sendLoginForm(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const success: boolean = await fetchLogin(email, password);

    if (success) {
      router.push("/explore");
    } else
      setError(true);
  }

  return (
    <div className="bg-[#FFFFFF] h-screen font-bold">
      <div>
        <Link href="/" className="flex justify-center text-[100px] text-black hover:text-[#424242]">Area</Link>
        <h1 className="flex justify-center text-[50px] text-black mb-10">Log in</h1>
        <form onSubmit={(e) => sendLoginForm(e)}>
          <div className="flex justify-center">
            <Mail onChange={setEmail} />
          </div>
          <div className="flex justify-center">
            <Password w={"300px"} onChange={setPassword} />
          </div>
          {error &&
            (<Alert variant="destructive" className="bg-red-100 rounded-4xl mb-[20px] mr-[20px] w-[300px] mx-auto">
              <AlertCircleIcon />
              <AlertTitle>Logins incorrect.</AlertTitle>
              <AlertDescription>
                <p>Your email or password seems to be wrong. Please try again.</p>
              </AlertDescription>
            </Alert>)
          }

          <div className="flex justify-center">
            <Link href="/passwords/forgot" className="flex justify-center mb-[30px] text-black text-center text-[20px] hover:text-[#676767] underline">
              Forgot your password ?
            </Link>
          </div>
          <div className="flex justify-center">
            <Button className="flex justify-center mb-3 bg-[#000000] text-white hover:text-black text-[40px] hover:bg-[#73bbff] rounded-full w-[350px] h-[100px] font-bold pt-2.5 hover:cursor-pointer" type="submit">
              Log in
            </Button>
          </div>
        </form>
        <p className="flex justify-center">Or</p>
        <div className="flex justify-center">
          <hr className="w-[350px] outline-[1px] mb-[30px]" style={{ color: "#4400ff" }} />
        </div>
        <div className="flex justify-center">
          <Button className="flex justify-center mb-[20px] bg-white text-black text-[30px] hover:bg-[#e4e4e4] rounded-full w-[450px] h-[70px] hover:border-[#000000] border-[#e4e4e4] border-[2px] outline-[1px] pt-[10px]" onClick={redirectOauthGithub}>
            Continue with Github
          </Button>
        </div>
        <div className="flex justify-center">
          <Button onClick={redirectOauthTodoist} className="flex justify-center mb-[20px] bg-black text-white text-[30px] hover:bg-[#3a3a3a] rounded-full w-[450px] h-[70px] hover:border-[#000000] border-[#e4e4e4] border-[2px] outline-[1px] pt-[10px]">
            Continue with Todoist
          </Button>
        </div>
        <p className="flex justify-center mb-3 text-black text-center text-[20px]">
          New to Area ? <Link href="/register" className="hover:text-[#4400ff] underline">Sign up here.</Link>
        </p>
      </div>
    </div>
  )
}
