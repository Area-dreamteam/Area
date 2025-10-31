/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** config
 */

export type triggerValue = { [key: string]: boolean }[] | string

export interface ConfigRespAct {
  name: string
  type: string
  values: triggerValue
}

export interface ConfigReqAct {
  name: string
  type: string
  values: string | string[]
}
