/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** config
*/

export interface ConfigRespAct
{
    name: string,
    type: string,
    values: { key: string, val: boolean }[] | string
}

export interface ConfigReqAct
{
    name: string,
    type: string,
    values: { key: string, val: boolean }[] | string[] | string
}