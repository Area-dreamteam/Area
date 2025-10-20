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
import { Button } from "@/components/ui/button"
import { fetchDeleteMyself, fetchMyself } from "@/app/functions/fetch"
import redirectToPage from "@/app/functions/redirections"
import MyProfileProp from "@/app/types/profile"

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
    profile: MyProfileProp | null;
}

function Profile({profile}: PersonnalInfoProp)
{
    // const [modifiedProfile, setModifiedprofile] = useState(profile);

    return (
        <div className="mx-auto mt-[40px] w-[700px] font-bold">
            <h1 className="centered text-[50px] mt-[40px] font-bold">
                Account Settings
            </h1>
            <hr/>
            {profileLabels("Account")}
            <br/>
            <h3>
                Username
            </h3>
            <Input defaultValue={profile?.name}/>
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
            <Input defaultValue={profile?.email}/>
            <br/><br/>
            {profileLabels("Linked accounts")}
            {LinkedAccount("Apple is not linked", "Link your account", "https://apple.com")}
            {LinkedAccount("Facebook is not linked", "Link your account", "https://facebook.com")}
            {LinkedAccount("Google is linked", "Unlink", "https://google.com")}
            <DeleteAccount/>
            <Button className="block mx-auto text-[40px] mt-[70px] text-white w-[300px] h-[100px] rounded-full font-bold mb-[20px]" disabled>
                Update
            </Button>
        </div>
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
                redirectToPage("/login");
        }
        fetchProfileData();
    }, []);

    return (
        <div>
            {available ?
                <Profile profile={profile}/>
            :
                <p className="centered text-[50px]">Loading...</p>
            }
        </div>
    )
}