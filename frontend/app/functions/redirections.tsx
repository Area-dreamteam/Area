/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** redirections
*/

import { redirect } from "next/navigation"

export default function redirectToPage(link: string)
{
    redirect(link);
}
