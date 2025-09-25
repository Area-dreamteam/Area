import type { Metadata } from "next";
import NavigationBar from "./components/Navbar"
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
        <NavigationBar/>
        {/* <link className="bg-black" rel="icon" href="../../public/menubar.png" sizes="48x48"/> */}
        {children}
      </body>
    </html>
  );
}
