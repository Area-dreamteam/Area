/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

export default function Settings()
{
    return (
        <div>
            <h1>
                Account Settings
            </h1>
            <h2>
                Profile
            </h2>
            <p>Personalize your account by linking a profile from another service.</p>
            <Button disabled>
                Add profile service
            </Button>
            <h2>
                Account
            </h2>
            <h3>
                Username
            </h3>
            <Input defaultValue="Pseudo"/>
            <h3>
                Username
            </h3>
            <Input defaultValue="Password" type="password"/>
            <Button>Change password</Button>
            <h3>
                Email
            </h3>
            <Input defaultValue="Email"/>
            <h3>
                Time zone
            </h3>
            <Input defaultValue="Pseudo"/>
            <Select>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="(+01:00) Paris" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="-10">(-10:00)</SelectItem>
                    <SelectItem value="-9">(-9:00)</SelectItem>
                    <SelectItem value="-8">(-8:00)</SelectItem>
                    <SelectItem value="-7">(-7:00)</SelectItem>
                    <SelectItem value="-6">(-6:00)</SelectItem>
                    <SelectItem value="-5">(-5:00)</SelectItem>
                    <SelectItem value="-4">(-4:00)</SelectItem>
                    <SelectItem value="-3">(-3:00)</SelectItem>
                    <SelectItem value="-2">(-2:00)</SelectItem>
                    <SelectItem value="-1">(-1:00)</SelectItem>
                    <SelectItem value="0">(0:00)</SelectItem>
                    <SelectItem value="+1">(+1:00)</SelectItem>
                    <SelectItem value="+2">(+2:00)</SelectItem>
                    <SelectItem value="+3">(+3:00)</SelectItem>
                    <SelectItem value="+4">(+4:00)</SelectItem>
                    <SelectItem value="+5">(+5:00)</SelectItem>
                    <SelectItem value="+6">(+6:00)</SelectItem>
                    <SelectItem value="+7">(+7:00)</SelectItem>
                    <SelectItem value="+8">(+8:00)</SelectItem>
                    <SelectItem value="+9">(+9:00)</SelectItem>
                    <SelectItem value="+10">(+10:00)</SelectItem>
                    <SelectItem value="+11">(+11:00)</SelectItem>
                    <SelectItem value="+12">(+12:00)</SelectItem>
                    <SelectItem value="+13">(+13:00)</SelectItem>
                </SelectContent>
            </Select>
            {/* to complete later because there's way to much to do here and it isn't on the to-do list for monday */}
        </div>
    )
}