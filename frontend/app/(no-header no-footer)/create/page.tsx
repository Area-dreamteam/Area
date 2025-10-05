/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { fetchServices } from "@/app/functions/fetch"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Service } from "@/app/types/service"
import { useState, useEffect } from "react"
import { redirect } from "next/navigation"
import Image from "next/image"

interface ChoiceButtonProp
{
    buttonText?: string,
    disable?: boolean,
    setIsChoosing: (data: boolean) => void,
}

function Action({buttonText = "", disable = false, setIsChoosing}: ChoiceButtonProp)
{
    return (
        <div className="mx-auto mt-[75px] w-[600px] h-[130px] rounded-xl text-white flex items-center justify-between px-[10px]" onClick={() => ""} style={{ background: (disable ? "grey" : "black")}}>
            <p className="flex-1 flex justify-center text-[80px]">
                {buttonText}
            </p>
            {!disable && 
                <Button className="mr-[20px] rounded-full text-black hover:bg-white bg-white hover:cursor-pointer px-[30px] py-[20px] font-bold w-[100px] text-[20px]" onClick={() => setIsChoosing(true)}>
                    Add
                </Button>
            }
        </div>
    )
}

interface UpButtonProp
{
    text: string,
    act: (param: any) => void,
    param: any
}

function LeftUpButton({text, act, param}: UpButtonProp)
{
    return (
        <Button className="ml-[40px] mt-[40px] rounded-full border-black text-black hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[120px] text-[20px]" onClick={() => act(param)}>
            {text}
        </Button>
    )
}

function Continue()
{
    return (
        <Button className="rounded-full border-black text-white hover:bg-black bg-black border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[250px] h-[100px] text-[30px]">
            Continue
        </Button>
    )
}

interface CreationProp
{
    action: any | null,
    reaction: any | null,
    setAction: (data: any) => void,
    setReaction: (data: any) => void,
    setChoosingAction: (data: boolean) => void,
    setChoosingReaction: (data: boolean) => void,
}

function Creation({action, reaction, setAction, setReaction,
    setChoosingAction, setChoosingReaction}: CreationProp)
{
    return (
        <div>
            <div className="grid grid-cols-4">
                <LeftUpButton text="Back" act={redirect} param={"/my_applets"}/>
                <p className="mt-[35px] flex flex-col text-[50px] font-bold col-span-2 text-center">
                    Create
                </p>
            </div>
            <Action buttonText="If This" setIsChoosing={setChoosingAction}/>
            <Action buttonText="Then That" disable={action == null}
                setIsChoosing={setChoosingReaction}/>
            <div className="flex justify-center mt-[100px]">
                {reaction != null &&
                    <Continue/>
                }
            </div>
        </div>
    )
}

interface SearchProp {
    search?: string
    services?: Service[] | null,
    className?: string,
    onClick?: (param: any) => void,
    arg: any
}

function ActionsPage()
{
    return (
        <div>
            Actions
        </div>
    )
}

function Services({search = "", services = null,
    className = "", onClick = () => ""}: SearchProp)
{
    if (services == null) {
        return (
            <p className="flex justify-center text-[20px] mt-[20px]">
                No service found.
            </p>
        )
    }

    const filteredServices = services.filter(service =>
        service.name.toLowerCase().includes(search.toLowerCase())
    );
    const nbServices = filteredServices.length;
    const serviceBlocks = services.map((service) => ((
        service.name.toLowerCase().includes(search.toLowerCase()) ?
        (
            <div key={service.id} className="rounded-xl w-[200px] h-[200px] hover:cursor-pointer relative" style={{ backgroundColor: service.color }} onClick={onClick}>
                { service.logo == "" || service.logo == null ? "" : (<Image alt="service's logo" src={service.logo} width={200} height={200} className="rounded-xl w-[200px] h-[200px]"/>)}
                <div className="flex justify-center">
                    <p className="font-bold text-white text-[20px] m-[20px]">{service.name}</p>
                </div>
            </div>
        ) : (
            ""
        )
    )))

    return (
        <div className="w-full">
            {nbServices != 0 ? (
                <div className={className}>
                    {serviceBlocks} 
                </div>
            ) : (
                <p className="flex justify-center text-[20px] mt-[20px]">
                    No service found.
                </p>
            )}
        </div>
    )
}

interface ChooseActProp
{
    choosingAction: boolean,
    choosingReaction: boolean,
    setChoosingAction: (data: boolean) => void,
    setChoosingReaction: (data: boolean) => void,
}

function ChooseAct({choosingAction, choosingReaction,
    setChoosingAction, setChoosingReaction}: ChooseActProp)
{
    const [search, setSearch] = useState("");
    const [services, setServices] = useState(null);
    const [chooseSelection, setChooseSelection] = useState(false);

    useEffect(() => {
        fetchServices(setServices);
    }, [])

    return (
        <div>
            {!chooseSelection &&
                <div>
                    <div className="grid grid-cols-4">
                        <LeftUpButton text="Cancel" act={choosingAction ? setChoosingAction : setChoosingReaction} param={false}/>
                        <p className="mt-[35px] flex flex-col text-[50px] font-bold col-span-2 text-center">
                            Choose a service
                        </p>
                    </div>
                    <Input className="w-[400px] mx-auto block mt-[50px] border-[4px] h-[50px] text-[20px] placeholder:text-[20px]" placeholder="Search services" onChange={(e) => setSearch(e.target.value)}/>
                    <Services search={search} services={services} className="mt-[50px] grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-8 w-fit mx-auto" onClick={setChooseSelection} arg={true}/>
                </div>
            }
            {chooseSelection &&
                <ActionsPage/>
            }
        </div>
    )
}

export default function Create()
{
    const [action, setAction] = useState(null);
    const [reaction, setReaction] = useState(null);
    const [choosingAction, setChoosingAction] = useState(false);
    const [choosingReaction, setChoosingReaction] = useState(false);

    return (
        <div>
        {(!choosingAction && !choosingReaction) &&
            <Creation action={action} reaction={reaction}
            setAction={setAction} setChoosingAction={setChoosingAction}
            setReaction={setReaction} setChoosingReaction={setChoosingReaction}/>
        }
        {choosingAction &&
            <ChooseAct
            choosingAction={choosingAction} choosingReaction={choosingReaction}
            setChoosingAction={setChoosingAction} setChoosingReaction={setChoosingReaction}
            />
        }
        {choosingReaction &&
            <ChooseAct
            choosingAction={choosingAction} choosingReaction={choosingReaction}
            setChoosingAction={setChoosingAction} setChoosingReaction={setChoosingReaction}
            />
        }
        </div>
    )
}