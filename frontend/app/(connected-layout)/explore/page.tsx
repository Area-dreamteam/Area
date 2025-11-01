/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** page
 */

'use client'

import { fetchServices, fetchApplets } from '@/app/functions/fetch'
import taskbarButton from '@/app/components/TaskBarButtons'
import Services from '@/app/components/Services'
import { Button } from '@/components/ui/button'
import Applets from '@/app/components/Applets'
import { Service } from '@/app/types/service'
import { PublicApplet, PrivateApplet } from '@/app/types/applet'
import { Input } from '@/components/ui/input'
import { useState, useEffect } from 'react'
import { redirect } from 'next/navigation'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuCheckboxItem,
} from '@radix-ui/react-dropdown-menu'

function customDropdown(
  text: string | null,
  disable: boolean,
  setFilter: (str: string | null) => void,
  id: number
) {
  if (id == -1)
    return ("");
  return (
    <DropdownMenuCheckboxItem
      key={id}
      className={`hover:bg-[#9ca2ff] hover:text-white pl-[5px] ${disable ? 'bg-[#0084ff] text-white' : ''} rounded-md`}
      onClick={() => setFilter(text)}
    >
      {text ? text : 'All services'}
    </DropdownMenuCheckboxItem>
  )
}

interface FilterProp {
  filter: string | null
  services: Service[] | null
  setFilter: (str: string | null) => void
}

function Filter({ services, filter, setFilter }: FilterProp) {
  const uniqueCategories = services
    ? Array.from(new Set(services.map((service) => service.category)))
    : []

  const dropdownFilters = uniqueCategories.map((category, index) => {
    return customDropdown(category, filter == category, setFilter, index)
  })

  return (
    <div className="centered">
      <DropdownMenu
        aria-label="You can filter according to the type of service you're looking for"
      >
        <DropdownMenuTrigger asChild>
          <Button className="ring-[2px] ring-black bg-white text-black text-[15px] hover:bg-white font-bold">
            {filter ? filter : 'All services'}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="bg-white rounded-md border-1 pl-[5px] pr-[5px]">
          <DropdownMenuLabel className="font-bold pb-[10px]">
            Filters
          </DropdownMenuLabel>
          {customDropdown(null, filter == null, setFilter, -1)}
          <DropdownMenuLabel className="font-bold pb-[10px]">
            Categories
          </DropdownMenuLabel>
          {dropdownFilters}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}

interface SearchProp {
  search?: string
  services?: Service[] | null
  applets?: (PublicApplet | PrivateApplet)[] | null
}

function All({ search = '', services = null, applets = null }: SearchProp) {
  return (
    <div>
      <h1 className="centered font-bold text-[25px]"> Services </h1>
      <Services
        search={search}
        services={services}
        className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center"
        boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer border-black border-[2px]"
        onClick={redirectToService}
      />
      <br />
      <h1 className="centered font-bold text-[25px]"> Applets </h1>
      <Applets
        search={search}
        applets={applets}
        className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center"
        boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer border-black border-[2px]"
        onClick={redirectToApplet}
      />
    </div>
  )
}

function redirectToService(service: Service) {
  redirect(`/services/${service.name}`)
}

function redirectToApplet(applet: PublicApplet | PrivateApplet) {
  redirect(`/applets/${applet.id}`)
}

export default function Explore() {
  const [page, setPage] = useState('All')
  const [searched, setSearched] = useState('')
  const [filter, setFilter] = useState<string | null>(null)
  const [applets, setApplets] = useState<
    (PublicApplet | PrivateApplet)[] | null
  >(null)
  const [services, setServices] = useState<Service[] | null>(null)

  useEffect(() => {
    fetchServices(setServices)
    fetchApplets(setApplets)
  }, [])

  return (
    <div>
      <h1 className="font-bold text-[100px] centered"> Explore </h1>
      <div className="centered">
        <div className="flex justify-around w-1/2">
          {taskbarButton('All', page, setPage, true)}
          {taskbarButton('Applets', page, setPage, true)}
          {taskbarButton('Services', page, setPage, true)}
        </div>
      </div>
      <br />
      <Input
        aria-label="You can search by name"
        className="mx-auto block w-[400px]"
        placeholder="Search Applets or Services"
        onChange={(e) => setSearched(e.target.value)}
      />
      <br />
      {page == 'Services' && (
        <Filter services={services} filter={filter} setFilter={setFilter} />
      )}
      <div className="centered">
        <div>
          {page == 'Services' && (
            <Services
              filter={filter}
              search={searched}
              services={services}
              className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center"
              boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer border-black border-[2px]"
              onClick={redirectToService}
            />
          )}
          {page == 'Applets' && (
            <Applets
              search={searched}
              applets={applets}
              className="mt-[50px] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 justify-items-center"
              boxClassName="rounded-xl w-[250px] h-[300px] hover:cursor-pointer"
              onClick={redirectToApplet}
            />
          )}
        </div>
        {page == 'All' && (
          <All search={searched} services={services} applets={applets} />
        )}
      </div>
    </div>
  )
}
