/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** service
*/

export interface Service {
    id: number;
    name: string;
    image_url: string;
    logo: string;
    color: string;
}

export interface SpecificService {
    id: number;
    name: string;
    description: string;
    image_url: string;
    logo: string;
    color: string;
}