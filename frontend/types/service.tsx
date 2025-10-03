/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** applet
*/

export type Service = {
    id: number,
    user_id: number,
    name: string,
    desc: string,
    color: string,
    logo: string,
};

export type ServicesFormat = Record<string, Service>;
