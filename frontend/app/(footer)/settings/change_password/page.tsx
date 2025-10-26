/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { fetchChangePassword } from "@/app/functions/fetch";
import { Password } from "@/app/components/Forms"
import { useState } from "react";
import Link from "next/link"

function sendForm(currentPassword: string, newPassword: string,
    confirmNewPassword: string)
{
    if (newPassword != confirmNewPassword)
        return; // create a warning instead
    fetchChangePassword(currentPassword, newPassword);
    return;
}

export default function changePassword()
{
    const [newPassword, setNewPassword] = useState<string>("");
    const [currentPassword, setCurrentPassword] = useState<string>("");
    const [confirmNewPassword, setConfirmNewPassword] = useState<string>("");

    return (
        <form className="mx-auto mt-[40px] w-[75%] font-bold" onSubmit={() => sendForm(currentPassword, newPassword, confirmNewPassword)}>
            <h1 className="title">
                Change password
            </h1>
            <hr/>
            <br/>
            <h3 className="subtitle mb-[5px]">
                Current password
            </h3>
            <Password onChange={setCurrentPassword}/>
            <Link href="/passwords/forgot" className="simple-text special-link">
                Forgot your password ?
            </Link>
            <br/><br/>
            <h3 className="subtitle mb-[5px]">
                New password
            </h3>
            <Password onChange={setNewPassword}/>
            <br/>
            <h3 className="subtitle mb-[5px]">
                Confirm new password
            </h3>
            <Password onChange={setConfirmNewPassword}/>
            <button className="rounded-button centered inverted px-[5%] py-[3%] mt-[5%]" type="submit" disabled={Password.length >= 8 && newPassword.length >= 8 && confirmNewPassword.length >= 8 && newPassword == confirmNewPassword}>
                Change
            </button>
            <Link href="/settings" className="centered activate-link mt-[3%] mb-[5%]">
                Cancel
            </Link>
        </form>
    )
}