/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Validation
*/

import { Button } from "@/components/ui/button"

interface ValidationProp
{
    arg: any,
    text: string,
    addToClass?: string,
    center?: boolean,
    clickAct: (status: any) => void
}
  
export default function ValidateButton({ addToClass = "", arg, text, center = true, clickAct }:
    ValidationProp)
{
    return (
        <Button className={`rounded-full border-black text-white hover:bg-black bg-black border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[250px] h-[100px] text-[30px] ${center ? "mx-auto block" : ""} ${addToClass}`} onClick={() => clickAct(arg)}>
        {text}
        </Button>
    )
}