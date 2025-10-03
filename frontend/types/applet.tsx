/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** applet
*/

export type Applet = {
    id: number;
    name: string;
    description: string;
    user: { name: string };
    created_at: string;
    color: string;
    activated: boolean;
};

export type AppletsFormat = Record<string, Applet>;
