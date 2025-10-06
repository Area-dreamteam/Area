/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { fetchServices, fetchActs } from "@/app/functions/fetch"
import { Service, Acts } from "@/app/types/service"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { redirect } from "next/navigation"
import Image from "next/image"

interface ChoiceButtonProp
{
    setIsChoosing: (data: boolean) => void,
    replacementText?: string,
    buttonText?: string,
    disable?: boolean,
    chosen: Acts | null,
}

function ActionButton({buttonText = "", replacementText = "", disable = false,
    setIsChoosing, chosen = null}: ChoiceButtonProp)
{
    return (
        <div className="mx-auto mt-[75px] w-[600px] h-[130px] rounded-xl text-white flex items-center justify-between px-[10px]" onClick={() => ""} style={{ background: (disable ? "grey" : "black")}}>
            <h1 className="flex-1 flex justify-center text-[80px]">
                {buttonText}
            {chosen ?
                <p className="ml-[20px] m-[40px] text-[20px]">{chosen.name}</p>
                :
                replacementText
            }
            </h1>
            {(!disable && !chosen) && 
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
    param: any,
    color?: string
}

function LeftUpButton({text, act, param, color = "black"}: UpButtonProp)
{
    return (
        <Button className={`ml-[40px] mt-[40px] rounded-full border-${color} text-${color} hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[120px] text-[20px]`} onClick={() => act(param)}>
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
    setChoosingAction: (data: boolean) => void,
    setChoosingReaction: (data: boolean) => void,
}

function Creation({action, reaction,
    setChoosingAction, setChoosingReaction}: CreationProp)
{
    return (
        <div>
            <div className="grid grid-cols-4">
                <LeftUpButton text="Cancel" act={redirect} param={"/my_applets"}/>
                <p className="mt-[35px] flex flex-col text-[50px] font-bold col-span-2 text-center">
                    Create
                </p>
            </div>
            <ActionButton buttonText="If " replacementText="This"
                setIsChoosing={setChoosingAction} chosen={action}/>
            <ActionButton buttonText="Then " replacementText="That" disable={action == null}
                setIsChoosing={setChoosingReaction} chosen={reaction}/>
            <div className="flex justify-center mt-[100px]">
                {reaction != null &&
                    <Continue/>
                }
            </div>
        </div>
    )
}

interface ActionPageProp extends ChooseActProp
{
    type: string,
    service: Service,
    setService: (arg: Service | null) => void
}

function chooseThisAct(setChoosingAction: (param: boolean) => void,
    setAction: (param: Acts | null) => void, act: Acts)
{
    setChoosingAction(false);
    setAction(act);
}

function ActionsPage({service, setService, setAction,
    setChoosingAction, type}: ActionPageProp)
{
    const [acts, setActs] = useState<Acts[] | null>(null);

    useEffect(() => {
        fetchActs(service.id, type, setActs);
    }, [])

    return (
        <div>
            <div className="grid grid-cols-4 text-white w-screen h-[450px] rounded-b-xl" style={{ background: service.color }}>
            <LeftUpButton text="Back" act={setService} param={null} color="white"/>
            <hr className="col-span-4 mb-[120px]"/>
            <div className="flex flex-col justify-end text-[35px] mb-[20px] font-bold col-span-4 mx-auto">
            {service.logo &&
                <Image alt="service's logo" src={service.logo} width={200} height={200} className="rounded-xl w-[250px] h-[250px]"/>
                    }
                    <p className="text-[60px] mb-[20px]">{service.name}</p>
                </div>
            </div>
            {acts && acts.length > 0 ? (
                <div className="mt-[25px] grid-cols-3">
                    {acts.map((act) => (
                        <div key={act.id} className="rounded-xl w-[200px] h-[200px] hover:cursor-pointer relative" style={{ backgroundColor: service.color }} onClick={() => chooseThisAct(setChoosingAction, setAction, act)}>
                            <div className="flex justify-center">
                                <p className="font-bold text-white text-[20px] m-[20px]">{act.name}<br/>{act.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <p className="flex justify-center text-[20px] mt-[20px]">
                    No actions found.
                </p>
            )}
        </div>
    )
}

interface SearchProp {
    search?: string
    services?: Service[] | null,
    className?: string,
    onClick?: (param: any) => void
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
            <div key={service.id} className="rounded-xl w-[200px] h-[200px] hover:cursor-pointer relative" style={{ backgroundColor: service.color }} onClick={() => onClick(service)}>
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
    type: string,
    choosingAction: boolean,
    setChoosingAction: (data: boolean) => void,
    setAction: (data: Acts | null) => void
}

function ChooseAct({choosingAction, setChoosingAction, setAction, type}: ChooseActProp)
{
    const [search, setSearch] = useState<string>("");
    const [services, setServices] = useState<Service[] | null>(null);
    const [selected, setSelected] = useState<Service | null>(null);

    useEffect(() => {
        fetchServices(setServices);
    }, [])

    return (
        <div>
            {!selected &&
                <div>
                    <div className="grid grid-cols-4">
                        <LeftUpButton text="Back" act={setChoosingAction} param={false}/>
                        <p className="mt-[35px] flex flex-col text-[50px] font-bold col-span-2 text-center">
                            Choose a service
                        </p>
                    </div>
                    <Input className="w-[400px] mx-auto block mt-[50px] border-[4px] h-[50px] text-[20px] placeholder:text-[20px]" placeholder="Search services" onChange={(e) => setSearch(e.target.value)}/>
                    <Services search={search} services={services} className="mt-[50px] grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-8 w-fit mx-auto" onClick={setSelected}/>
                </div>
            }
            {selected &&
                <ActionsPage service={selected} setService={setSelected}
                choosingAction={choosingAction} setAction={setAction}
                setChoosingAction={setChoosingAction} type={type}/>
            }
        </div>
    )
}

export default function Create()
{
    const [action, setAction] = useState<Acts | null>(null);
    const [reaction, setReaction] = useState<Acts | null>(null);
    const [choosingAction, setChoosingAction] = useState(false);
    const [choosingReaction, setChoosingReaction] = useState(false);

    return (
        <div>
        {(!choosingAction && !choosingReaction) &&
            <Creation action={action} reaction={reaction}
            setChoosingAction={setChoosingAction}
            setChoosingReaction={setChoosingReaction}/>
        }
        {choosingAction &&
            <ChooseAct setAction={setAction} type="actions"
            choosingAction={choosingAction}
            setChoosingAction={setChoosingAction}
            />
        }
        {choosingReaction &&
            <ChooseAct setAction={setReaction} type="reactions"
            choosingAction={choosingReaction}
            setChoosingAction={setChoosingReaction}
            />
        }
        </div>
    )
}