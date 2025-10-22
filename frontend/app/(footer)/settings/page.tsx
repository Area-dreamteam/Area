/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import Link from "next/link"
import { useState, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { fetchDeleteMyself, fetchMyself, fetchUpdateMyself } from "@/app/functions/fetch"
import { MyProfileProp, UpdateProfileProp } from "@/app/types/profile"
import { redirect } from "next/navigation"

// function profileButton(text: string, _enable: boolean)
// {
//     return (
//         <Button>
//             {text}
//         </Button>
//     )
// }

function profileLabels(text: string)
{
    return (
        <h2 className="text-[30px] mt-[40px] font-bold">
            {text}
        </h2>
    )
}

function profileLink(text: string, ref: string, linkColor: string)
{
    return (
        <Link href={ref} className="mb-[30px] text-center text-[18px]" style={{ color: linkColor }}>
            {text}
        </Link>
    )
}

function DeleteAccount()
{
    return (
        <Link href={"/"} className="mb-[30px] text-center text-[18px]" style={{ color: "#ff0000" }} onClick={fetchDeleteMyself}>
            Delete my account
        </Link>
    )
}

function LinkedAccount(text: string, button: string, link: string)
{
    return (
        <div className="flex justify-around">
            {text}
            {profileLink(button, link, "#0099ff")}
        </div>
    )
}

interface PersonnalInfoProp
{
    profile: MyProfileProp;
}

function Profile({profile}: PersonnalInfoProp)
{
    const [personalProfile, setProfile] = useState<MyProfileProp>(profile);
    const [email, setEmail] = useState<string>((profile.email));
    const [name, setName] = useState<string>((profile.name));
  
    async function sendForm(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const success: boolean = await fetchUpdateMyself({name, email}, setProfile);
    }

    return (
        <form onSubmit={sendForm} className="mx-auto mt-[40px] w-[75%] font-bold">
            <h1 className="title mt-[40px] font-bold">
                Account Settings
            </h1>
            <hr/>
            {profileLabels("Account")}
            <br/>
            <h3>
                Username
            </h3>
            <Input defaultValue={personalProfile.name} onChange={(e) => setName(e.target.value)}/>
            <br/><br/>
            <h3>
                Password
            </h3>
            <Input defaultValue="********" type="password" readOnly/>
            {profileLink("Change password", "/settings/change_password", "#0099ff")}
            <br/><br/>
            <h3>
                Email
            </h3>
            <Input defaultValue={personalProfile.email} onChange={(e) => setEmail(e.target.value)}/>
            <br/><br/>
            {profileLabels("Linked accounts")}
            {LinkedAccount("Apple is not linked", "Link your account", "https://apple.com")}
            {LinkedAccount("Facebook is not linked", "Link your account", "https://facebook.com")}
            {LinkedAccount("Google is linked", "Unlink", "https://google.com")}
            <DeleteAccount/>
            <button className="rounded-button block mx-auto mt-[10%] mb-[10%] px-[5%] py-[2%] rounded-full inverted hover:cursor-pointer" type="submit">
                Update
            </button>
        </form>
    )
}

export default function Settings()
{
    const [available, setAvailable] = useState<boolean>(false);
    const [profile, setProfile] = useState<MyProfileProp | null>(null);

    useEffect(() => {
        const fetchProfileData = async () => {
            const succeed = await (fetchMyself(setProfile));
            console.log(profile);
            if (succeed)
                setAvailable(true);
            else
                redirect("/login");
        }
        fetchProfileData();
    }, []);

    return (
        <div>
            {available && profile ?
                <Profile profile={profile}/>
            :
                <p className="centered text-[50px]">Loading...</p>
            }
        </div>
    )
}
