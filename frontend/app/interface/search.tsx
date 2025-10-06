/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** search
*/

import { Applet } from "../types/applet"
import { Service } from "../types/service"

export interface SearchProp {
    search?: string
    widgets?: Applet[] | Service[] | null,
    className?: string,
    boxClassName?: string,
    onClick?: (param: any) => void
}