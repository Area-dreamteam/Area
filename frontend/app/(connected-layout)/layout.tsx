/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** layout
 */
import { ConnectedNavbar } from '../components/Navbar'

export default function ExploreLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <div>
      <ConnectedNavbar />
      {children}
    </div>
  )
}
