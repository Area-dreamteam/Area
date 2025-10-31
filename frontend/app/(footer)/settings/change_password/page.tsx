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
import { redirect } from 'next/navigation'
import { useState } from 'react'
import Link from 'next/link'

async function sendForm(
  currentPassword: string,
  newPassword: string,
  confirmNewPassword: string,
  setError: (arg: boolean) => void
) {
  if (newPassword !== confirmNewPassword) {
    setError(true)
    return false
  }
  console.log('same password')
  await fetchChangePassword(currentPassword, newPassword)
  redirect('/settings')
}

export default function changePassword() {
  const [error, setError] = useState<boolean>(false)
  const [newPassword, setNewPassword] = useState<string>('')
  const [currentPassword, setCurrentPassword] = useState<string>('')
  const [confirmNewPassword, setConfirmNewPassword] = useState<string>('')

  return (
    <div className="mx-auto mt-[40px] w-[75%] font-bold">
      <h1 className="title">Change password</h1>
      <hr />
      <br />
      <h3 className="subtitle mb-[5px]">Current password</h3>
      <Password onChange={setCurrentPassword} secure={false} />
      <Link href="/passwords/forgot" className="simple-text special-link">
        Forgot your password ?
      </Link>
      <br />
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
        className="rounded-button centered inverted px-[5%] py-[3%] mt-[5%] disabled:bg-gray-400 disabled:cursor-auto"
        disabled={
          newPassword.length < 8 ||
          confirmNewPassword.length < 8 ||
          newPassword.length != confirmNewPassword.length
        }
        onClick={() => {
          if (
            !sendForm(
              currentPassword,
              newPassword,
              confirmNewPassword,
              setError
            )
          ) {
            console.log(error)
          }
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
