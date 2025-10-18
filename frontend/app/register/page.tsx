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
import { useEffect, useState } from "react"
import Image from "next/image"
import Link from "next/link"
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
import redirectToPage from "../functions/redirections"
import { fetchAvailableOAuth, OAuthInfo, redirectOauth } from "../functions/oauth"

export default function Register() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [error, setError] = useState(false);
  const [password, setPassword] = useState("");
  const [logins, setLogins] = useState<[OAuthInfo]>();

  useEffect(() => {
    fetchAvailableOAuth(setLogins)
  }, [])


  async function sendRegisterForm(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const success: boolean = await fetchRegister(email, password);

    if (success)
      router.push("/login");
    else
      setError(true);
  }

  return (
    <div className="bg-white h-screen font-bold">
      <div>
        <p onClick={() => redirectToPage("/")} className="w-[200px] mx-auto centered title logo">Area</p>
        <h1 className="title text-black md:mb-10 mb-5">Register</h1>
        <form onSubmit={(e) => sendRegisterForm(e)}>
          <div className="centered md:mb-3 mb-1">
            <Mail onChange={setEmail} />
          </div>
          <div className="centered">
            <Password w={"300px"} onChange={setPassword} />
          </div>
          {error &&
            <Alert variant="destructive" className="bg-red-100 rounded-4xl mb-5 mr-[20px] w-[300px] mx-auto">
              <AlertCircleIcon />
              <AlertTitle>Sorry, this account already exist.</AlertTitle>
            </Alert>
          }
          <div className="centered">
            <button className="rounded-button inverted m-[5%]" type="submit">
              Get started
            </button>
          </div >
        </form>
      </div>
      <p className="centered mb-[2%] simple-text">Or</p>
      <div className="centered">
        <hr className="w-[40%] mb-[2%]" style={{ color: "#4400ff" }} />
      </div>
      <li>
        {logins && logins.map((l) => {
          return (
            <ul className="centered" key={l.name}>
              <button onClick={() => { redirectOauth(l.name) }} className="rounded-button border-1 m-[5%]" >
                Continue with {l.name}
              </button>
            </ul>
          )
        })}
      </li>
      <div className="centered">
        <p className="mb-[10%] text-black text-center simple-text">
          Already have an account ?
          <Link href="/login" className="activate-link">
            Log in here.
          </Link>
        </p>
      </div>
    </div>
  )
}
