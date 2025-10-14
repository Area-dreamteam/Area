/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** search
*/

import { Timestamp } from "next/dist/server/lib/cache-handlers/types"
import { Service } from "../types/service"

export interface Applet {
  id: number,
  name: string,
  description: string,
  user: {
    id: number,
    name: string
  },
  enable: boolean,
  created_at: Timestamp,
  color: string
}

export interface SearchProp {
  search?: string
  services?: Service[] | null
  applets?: Applet[] | null
}

