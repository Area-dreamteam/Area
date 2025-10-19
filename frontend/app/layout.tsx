/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** layout
*/

import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Area",
  description: "Build your own reactions chains",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
