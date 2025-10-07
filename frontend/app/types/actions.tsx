/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** actions
*/

export interface SpecificAction
{
    id: number,
    name: string,
    description: string,
    config_schema: [
      {
        name: string,
        type: string,
        values: string[]
      }
    ],
    service: {
      id: number,
      name: string,
      image_url: string,
      category: string,
      color: string
    }
}

export interface SpecificReaction
{
    id: number,
    name: string,
    description: string,
    config_schema: string,
    service: {
      id: number,
      name: string,
      image_url: string,
      category: string,
      color: string
    }
}
