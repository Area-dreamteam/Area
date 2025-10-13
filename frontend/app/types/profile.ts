/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** profile
*/

export default interface MyProfileProp
{
  id: number,
  name: string,
  email: string,
  role: string,
  user_services: [
    {
      id: number,
      name: string,
      image_url: string,
      color: string,
      connected: boolean
    }
  ]
}