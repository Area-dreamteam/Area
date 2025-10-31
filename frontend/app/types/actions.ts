/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** actions
 */

import { ConfigReqAct } from './config'

export interface SpecificAction {
  id: number
  name: string
  description: string
  config_schema: ConfigReqAct[]
  service: {
    id: number
    name: string
    image_url: string
    category: string
    color: string
  }
}

export interface SpecificReaction {
  id: number
  name: string
  description: string
  config_schema: ConfigReqAct[]
  service: {
    id: number
    name: string
    image_url: string
    category: string
    color: string
  }
}
