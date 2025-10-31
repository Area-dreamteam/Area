/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** service
 */

import { ConfigRespAct } from "./config";

export interface Act {
  id: number
  name: string
  description: string
}

export interface ActDetails {
  id: number,
  act: Act,
  config: ConfigRespAct[],
}

export interface Service {
  id: number
  name: string
  image_url: string
  category: string
  color: string
}

export interface SpecificService {
  id: number
  name: string
  description: string
  image_url: string
  category: string
  color: string
  oauth_required: boolean
}

export interface OAuth_login {
  name: string
  color: string
  image_url: string
}
