/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** search
*/

import { PublicApplet } from "../types/applet"
import { Service } from "../types/service"

export interface ServiceSearchProp {
    search?: string,
    filter?: string | null,
    services?: Service[] | null,
    className?: string,
    boxClassName?: string,
    onClick?: (param: any) => void
}

export interface AppletSearchProp {
    search?: string,
    filter?: string | null,
    applets?: PublicApplet[] | null,
    className?: string,
    boxClassName?: string,
    onClick?: (param: any) => void
}