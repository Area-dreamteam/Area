/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** page
 */

'use client'

import { fetchChangePassword } from '@/app/functions/fetch'
import { Password } from '@/app/components/Forms'
import Warning from '@/app/components/Warning'
import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

async function sendForm(
  currentPassword: string,
  newPassword: string,
  confirmNewPassword: string,
  setError: (arg: boolean) => void
) {
  if (newPassword !== confirmNewPassword) {
    setError(true);
    return false;
  }
  await fetchChangePassword(currentPassword, newPassword);
  return true;
}

export default function changePassword() {
  const [error, setError] = useState<boolean>(false)
  const [newPassword, setNewPassword] = useState<string>('');
  const [currentPassword, setCurrentPassword] = useState<string>('');
  const [confirmNewPassword, setConfirmNewPassword] = useState<string>('');
  const router = useRouter();

  return (
    <div className="mx-auto mt-[40px] w-[75%] font-bold">
      <h1 className="title">Change password</h1>
      <hr />
      <br />
      <h3 className="subtitle mb-[5px]">Current password</h3>
      <Password onChange={setCurrentPassword}/>
      <br />
      <h3 className="subtitle mb-[5px]">New password</h3>
      <Password onChange={setNewPassword} />
      <br />
      <h3 className="subtitle mb-[5px]">Confirm new password</h3>
      <Password onChange={setConfirmNewPassword} />
      {error &&
        Warning(
          'Invalid passwords',
          "New password and confirmation aren't the same"
        )}
      <button
        aria-label={`Click here to validate your changes. Currently, you ${
          newPassword.length < 8 ||
          confirmNewPassword.length < 8 ||
          newPassword.length != confirmNewPassword.length ? "can't" : "can"} validate your modifications${newPassword.length < 8 || confirmNewPassword.length < 8 ? " because your new password isn't greater than 8 characters" : ""} ${newPassword.length != confirmNewPassword.length ? `${(newPassword.length < 8 || confirmNewPassword.length < 8) ? " and" : " because"} both passwords you entered to modify the old one aren't the same. Please enter the same password in the new password input and the confirmation input` : ""}.`}
        className="rounded-button centered inverted px-[5%] py-[3%] mt-[5%] disabled:bg-gray-400 disabled:cursor-auto"
        disabled={
          newPassword.length < 8 ||
          confirmNewPassword.length < 8 ||
          newPassword.length != confirmNewPassword.length
        }
        onClick={async () => {
          const state = await sendForm(
              currentPassword,
              newPassword,
              confirmNewPassword,
              setError
              );
            if (state)
              router.push("/settings")
        }}
      >
        Change
      </button>
      <Link href="/settings" className="centered activate-link mt-[3%] mb-[5%]">
        Cancel
      </Link>
    </div>
  )
}
