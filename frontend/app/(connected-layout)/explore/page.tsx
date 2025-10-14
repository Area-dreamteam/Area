/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { Timestamp } from "next/dist/server/lib/cache-handlers/types"
import { fetchServices, fetchApplets } from "@/app/functions/fetch"
import taskbarButton from "@/app/components/TaskBarButtons"
import Services from "@/app/components/Services"
import { Button } from "@/components/ui/button"
import Applets from "@/app/components/Applets"
import { Service } from "@/app/types/service"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { redirect } from "next/navigation"
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuCheckboxItem,
} from "@radix-ui/react-dropdown-menu"
import { Applet, SearchProp } from "@/app/interface/search"

function customDropdown(text: string) {
  return (
    <DropdownMenuCheckboxItem className="hover:bg-[#a5c1e5] pl-[5px] rounded-md">
      {text}
    </DropdownMenuCheckboxItem>
  )
}

function Filter() {
  return (
    <div className="flex justify-center">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button className="ring-[2px] ring-black bg-white text-black text-[15px] hover:bg-white font-bold">
            All services
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="bg-white rounded-md border-1 pl-[5px] pr-[5px]">
          <DropdownMenuLabel className="font-bold pb-[10px]">Filters</DropdownMenuLabel>
          {customDropdown("All services")}
          {customDropdown("New services")}
          {customDropdown("Popular services")}
          <DropdownMenuLabel className="font-bold pb-[1px]">Categories</DropdownMenuLabel>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}

function All({ search = "", services = null, applets = null }: SearchProp) {
  return (
    <div>
      <h1 className="flex justify-center font-bold text-[25px]"> Services </h1>
      <Services search={search} widgets={services} className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer" onClick={redirectToService} />
      <br />
      <h1 className="flex justify-center font-bold text-[25px]"> Applets </h1>
      <Applets search={search} widgets={applets} className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer" onClick={redirectToApplet} />
    </div>
  )
}

function redirectToService(service: Service) {
  redirect(`/services/${service.name}`);
}

function redirectToApplet(applet: Applet) {
  redirect(`/applets/${applet.name}`);
}

export default function Explore() {
  const [page, setPage] = useState("All");
  const [searched, setSearched] = useState("");
  const [services, setServices] = useState(null);
  const [applets, setApplets] = useState(null);

  useEffect(() => {
    fetchServices(setServices);
    fetchApplets(setApplets);
  }, [])

  return (
    <div>
      <h1 className="font-bold text-[100px] flex justify-center"> Explore </h1>
      <div className="flex justify-center">
        <div className="flex justify-around w-1/2">
          {taskbarButton("All", page, setPage, true)}
          {taskbarButton("Applets", page, setPage, true)}
          {taskbarButton("Services", page, setPage, true)}
        </div>
      </div>
      <br />
      <Input className="mx-auto block w-[400px]" placeholder="Search Applets or Services" onChange={(e) => setSearched(e.target.value)} />
      <br />
      {page == "Services" && <Filter />}
      <div className="flex justify-center">
        {page == "Services" && <Services search={searched} widgets={services} className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer" onClick={redirectToService} />}
        {page == "Applets" && <Applets search={searched} widgets={applets} className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center" boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer" onClick={redirectToApplet} />}
        {page == "All" && <All search={searched} services={services} applets={applets} />}
      </div>
    </div>
  )
}
