/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** cookies
*/

export default function getCookies(name: string): string | null {
    
    if (typeof document === 'undefined')
        return null;
    
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    
    if (parts.length === 2) {
      return parts.pop()?.split(';').shift() || null;
    }
    
    return null;
  }