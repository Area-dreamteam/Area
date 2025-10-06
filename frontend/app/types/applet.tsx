/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** service
*/

import { Timestamp } from "next/dist/server/lib/cache-handlers/types";

export interface Applet {
    id: number;
    name: string;
    image_url: string;
    logo: string;
    color: string;
}

export interface SpecificApplet {
    id: number,
    name: string,
    description: string,
    user: {
      id: number,
      name: string
    },
    created_at: Timestamp,
    color: string
}
