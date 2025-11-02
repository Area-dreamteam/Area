/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** service
 */

import { Timestamp } from 'next/dist/server/lib/cache-handlers/types'
import { ConfigRespAct } from './config'

export interface Applet {
  id: number
  name: string
  description: string
  user: {
    id: number
    name: string
  }
  enable: boolean
  created_at: Timestamp
  color: string
}

export interface AppletRespSchema {
  name: string,
  description: string,
  action: {
    action_id: number,
    config: ConfigRespAct[]
  }
  reactions:
  {
    reaction_id: number,
    config: ConfigRespAct[]
  }[]
}

export interface PublicApplet {
  id: number
  name: string
  description: string
  user: {
    id: number
    name: string
  }
  created_at: Timestamp
  color: string
}

export interface PrivateApplet {
  id: number
  name: string
  description: string
  user: {
    id: number
    name: string
  }
  enable: true
  created_at: Timestamp
  color: string
}

export interface SpecificPublicApplet {
  area_info: {
    id: number
    name: string
    description: string
    user: {
      id: number
      name: string
    }
    created_at: Timestamp
    color: string
  }
  action: {
    id: number
    name: string
    description: string
    service: {
      id: number
      name: string
      image_url: string
      category: string
      color: string
    }
  }
  reactions:
    {
      id: number
      name: string
      description: string
      service: {
        id: number
        name: string
        image_url: string
        category: string
        color: string
      }
    }[],
}

export interface SpecificPrivateApplet {
  area_info: {
    id: number
    name: string
    description: string
    user: {
      id: number
      name: string
    }
    enable: boolean
    created_at: Timestamp
    color: string
  }
  action: {
    id: number
    name: string
    description: string
    service: {
      id: number
      name: string
      image_url: string
      category: string
      color: string
    }
    config: ConfigRespAct[]
  }
  reactions:
    {
      id: number
      name: string
      description: string
      service: {
        id: number
        name: string
        image_url: string
        category: string
        color: string
      }
      config: ConfigRespAct[]
    }[],
}
