/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { fetchDeleteMyself, fetchDisconnectOauth, fetchMyself, fetchUpdateMyself } from "@/app/functions/fetch"
import { MyProfileProp, OauthProfileProp } from "@/app/types/profile"
import { redirectOauth } from "@/app/functions/oauth"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { redirect } from "next/navigation"
import Link from "next/link"

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
        <Link href={ref} className="special-link" style={{ color: linkColor }}>
            {text}
        </Link>
    )
}

async function disconnectOauth(oauthId: number, setUpdate: (arg: boolean) => void)
{
    await fetchDisconnectOauth(oauthId);
    setUpdate(true);
}

async function connectOauth(oauthName: string, setUpdate: (arg: boolean) => void)
{
    await redirectOauth(oauthName, null);

    window.addEventListener("message", (event) => {
        console.log(event.data);
        if (event.data.type === `${oauthName}_login_complete`) {
            setUpdate(true);
        }
    });
}

function oauthLink(user: MyProfileProp, service: OauthProfileProp,
    linkColor: string, setUpdate: (arg: boolean) => void)
{
    return (
        <p className="special-link simple-text hover:cursor-pointer" style={{ color: linkColor }} onClick={() => (service.connected ? disconnectOauth(service.id, setUpdate) : connectOauth(service.name, setUpdate))}>
            {service.connected ? "Unlink" : "Link your account"}
        </p>
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

function LinkedAccounts(user: MyProfileProp, setUpdate: (arg: boolean) => void)
{
    const linked = user.oauth_login.map((service) => {
        return (
            <div key={service.id} className="grid grid-cols-2 gap-5 mb-[2%]">
                <p className="simple-text"> {service.name} </p>
                {oauthLink(user, service, "#0099ff", setUpdate)}
            </div>
        )
    })

    return (
        <div className="w-[75%] block mx-auto mb-5 mt-5">
            {linked}
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
    const [user, setUser] = useState<MyProfileProp | null>(null);
    const [name, setName] = useState<string>((profile.name));
    const [update, setUpdate] = useState<boolean>(true);
  
    async function sendForm(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        await fetchUpdateMyself({name, email}, setProfile);
    }

    useEffect(() => {
        if (!update)
            return
        const getPersonalInfos = async () => {
            await fetchMyself(setUser);
        }
        getPersonalInfos();
        setUpdate(false);
    }, [update]);

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
            {user ? LinkedAccounts(user, setUpdate) : ""}
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
