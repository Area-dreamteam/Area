/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** profile
 */

export interface OauthProfileProp {
  id: number
  name: string
  image_url: string
  color: string
  connected: boolean
}

export interface MyProfileProp {
  id: number
  name: string
  email: string
  role: string
  oauth_login: [OauthProfileProp]
}

export interface UpdateProfileProp {
  name: string
  email: string
}
