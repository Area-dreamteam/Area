/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Logins
*/

'use client'

import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
import Link from "next/link"
import { useEffect, useState } from "react"
import { redirect, useRouter } from "next/navigation"
import { AlertCircleIcon } from "lucide-react"
import { Password, Mail } from "../components/Forms"
import { fetchLogin, fetchRegister } from "../functions/fetch"
import { fetchAvailableOAuth, OAuthInfo, redirectOauth } from "../functions/oauth"

export default function Logins(isRegister: boolean)
{
    const router = useRouter();
    const [email, setEmail] = useState<string>("");
    const [error, setError] = useState<boolean>(false);
    const [password, setPassword] = useState<string>("");
    const [logins, setLogins] = useState<[OAuthInfo]>();
  
    async function sendForm(e: React.FormEvent<HTMLFormElement>) {
      e.preventDefault();
      const success: boolean = await (isRegister ? fetchRegister(email, password) : fetchLogin(email, password));
  
      if (success) {
        router.push("/explore");
      } else
        setError(true);
    }

    useEffect(() => {
      fetchAvailableOAuth(setLogins)
    }, []);

    return (
        <div className="font-bold">
            <p onClick={() => redirect("/")} className="w-[200px] mx-auto centered title logo">
                Area
            </p>
            <h1 className="title text-black sm:mb-10 mb-5">
                {isRegister ? "Register" : "Log in"}
            </h1>
            <form onSubmit={(e) => sendForm(e)}>
                <div className="centered sm:mb-3 mb-1">
                    <Mail onChange={setEmail} />
                </div>
                <div className="centered">
                    <Password onChange={setPassword}/>
                </div>
                {error &&
                    <Alert variant="destructive" className="bg-red-100 rounded-4xl mb-5 mr-[20px] w-[300px] mx-auto">
                    <AlertCircleIcon />
                    <AlertTitle>
                        {isRegister ? "Sorry, this account already exist" : "Logins incorrect"}.
                    </AlertTitle>
                    {!isRegister &&
                        <AlertDescription>
                            <p>Your email or password seems to be wrong. Please try again.</p>
                        </AlertDescription>
                    }
                    </Alert>
                }
                {!isRegister &&
                    <Link href="/passwords/forgot" className="centered simple-text activate-link sm:mt-4 mt-2">
                        Forgot your password ?
                    </Link>
                }
                <div className="centered">
                    <button className="rounded-button inverted m-[5%]" type="submit">
                    {isRegister ? "Get started" : "Log in"}
                    </button>
                </div >
            </form>
            <p className="centered mb-[2%] simple-text">Or</p>
            <div className="centered">
                <hr className="w-[40%] mb-[2%]" style={{ color: "#4400ff" }} />
            </div>
            <li className="mb-[5%]">
                {logins && logins.map((log) => {
                    return (
                        <ul className="centered" key={log.name}>
                            <button onClick={() => { redirectOauth(log.name, "/explore") }} className="rounded-button inverted border-1 mt-[2%]" >
                                Continue with {log.name.replace("Oauth", "")}
                            </button>
                        </ul>
                    )
                })}
            </li>
            <p className="mb-[10%] text-black text-center simple-text">
                {isRegister ?  "Already have an account ?" : "New to Area ?"}
                {isRegister ? (
                    <Link href="/login" className="activate-link">
                    Log in here.
                    </Link>
                ) : (
                    <Link href="/register" className="activate-link">
                    Sign up here.
                    </Link>
                )}
            </p>
        </div>
    )
}