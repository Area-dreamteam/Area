/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** images
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api/backend';

export function getImageUrl(imagePath: string): string {
  if (!imagePath || imagePath === '.' || imagePath.trim() === '') return '';
  
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }
  
  const cleanPath = imagePath.startsWith('/') ? imagePath.slice(1) : imagePath;
  
  return `${API_BASE_URL}/${cleanPath}`;
}

export function getServiceImageUrl(service: { image_url: string }): string {
  return getImageUrl(service.image_url);
}
