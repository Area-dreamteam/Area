/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** layout
 */

import NavigationBar from '../components/Navbar'

export default function DisconnectedLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <div>
      <NavigationBar />
      {children}
    </div>
  )
}
