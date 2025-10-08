/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { fetchCreateApplet, fetchServices, fetchAction, fetchActs } from "@/app/functions/fetch"
import { ConfigRespAct, ConfigReqAct } from "@/app/types/config"
import { Service, Act } from "@/app/types/service"
import Services from "@/app/components/Services"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { redirect } from "next/navigation"
import Image from "next/image"
import { SpecificAction, SpecificReaction } from "@/app/types/actions"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"
  import { Checkbox } from "@/components/ui/checkbox"

//-- Buttons --//

interface ChoiceButtonProp
{
    setIsChoosing: (data: boolean) => void,
    replacementText?: string,
    buttonText?: string,
    disable?: boolean,
    chosen: Act | null,
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

interface ValidationProp
{
    text: string,
    setValidating: (status: boolean) => void
}

function ValidateButton({text, setValidating}: ValidationProp)
{
    return (
        <Button className="rounded-full border-black text-white hover:bg-black bg-black border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[250px] h-[100px] text-[30px]" onClick={() => setValidating(true)}>
            {text}
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

//-- Send form --//

function createApplet(action: Act, reaction: Act, title: string)
{
    fetchCreateApplet(action, reaction, title);
    // redirect to the page created then
}

//-- Creation page --//

function Creation({action, reaction,
    setChoosingAction, setChoosingReaction}: CreationProp)
{
    const [validating, setValidating] = useState<boolean>(false);
    const [title, setTitle] = useState<string>(`if ${action?.name}, then ${reaction?.name}`);

    return (
        <div>
            {validating ? (
                <div>
                    <div className="rounded-b-xl bg-black text-white font-bold w-screen h-[450px]">
                        <div className="grid grid-cols-4">
                            <LeftUpButton text="Back" act={setValidating} param={false} color="white"/>
                            <p className="mt-[35px] flex flex-col text-[50px] col-span-2 text-center">
                                Review and finish
                            </p>
                            <hr className="col-span-4 mb-[120px]"/>
                        </div>
                        <p className="text-white flex justify-center mb-[20px]">Applet Title</p>
                        <Input className="block mx-auto w-[500px] h-[70px] bg-white text-black" defaultValue={title} onChange={(e) => setTitle(e.target.value)}/>
                    </div>
                    <div className="flex justify-center mt-[30px]">
                        <Button className="rounded-full border-black text-white hover:bg-black bg-black border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[250px] h-[100px] text-[30px]" onClick={() => createApplet(action, reaction, title)}>
                            Finish
                        </Button>
                    </div>
                </div>
            ):(
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
                            <ValidateButton setValidating={setValidating} text="Continue"/>
                        }
                    </div>
                </div>
            )}
        </div>
    )
}

//-- Affichage des triggers --//

interface SelectElementProp
{
    content: string[]
}

function SelectElement({content}: SelectElementProp)
{
    const selectItemsBlock = content.map((value) =>
        <SelectItem key={value} value={value}>{value}</SelectItem>
    );
    const [selectedValue, setSelectedValue] = useState<string>(content[0]);
// create the selected value before and stop displaying the display trigger and go back to create principale page with all infos
    return (
        <Select onValueChange={setSelectedValue} value={selectedValue}>
            <SelectTrigger className="w-[250px] text-black bg-white">
                <SelectValue placeholder={selectedValue}/>
            </SelectTrigger>
            <SelectContent className="text-black">
                <SelectGroup>
                    {selectItemsBlock}
                </SelectGroup>
            </SelectContent>
        </Select>
    )
}

interface TriggerProp
{
    config: string | ConfigReqAct[]
}

function DisplayTrigger({config}: TriggerProp)
{
    if (typeof config === "string")
        return ("");
    return (
        <div>
            <p className="mt-[20px] text-[20px] text-center">
                {config[0].name}
            </p>
            {(config[0].type == "select" && Array.isArray(config[0].values)
                && config[0].values.every(v => typeof v === "string")) &&
                <div className="flex justify-center">
                    <SelectElement content={config[0].values}/>
                </div>
            }
            {config[0].type == "input" &&
                <Input/>
            }
            {/* {(config.type == "check_list" && Array.isArray(config.values)
            && typeof config.values[0] === "object") &&
                <CheckBox/>
            } */}
        </div>
    )
}

//-- Choosing the trigger --//

interface chooseTriggerProp
{
    act: Act,
    type: string,
    service: Service,
    setChoosingTrigger: (arg: boolean) => void,
    setConfig: (arg: ConfigRespAct | null) => (void)
}

function ChooseTrigger({act, service, type, setConfig, setChoosingTrigger}: chooseTriggerProp)
{
    const [trigger, setTrigger] = useState<SpecificAction | SpecificReaction | null>(null);

    useEffect(() => {
        fetchAction(service.id, type, setTrigger);
    }, []);

    return (
        <div className="text-white w-screen h-screen" style={{ background: service.color }}>
            <div className="grid grid-cols-4 " >
                <LeftUpButton text="Back" act={setChoosingTrigger} param={false} color="white"/>
                <p className="mt-[35px] flex flex-col text-[50px] font-bold col-span-3 text-center">
                    Complete trigger fields
                </p>
                <hr className="col-span-4 mb-[20px]"/>
                <div className="flex flex-col text-[35px] mb-[20px] font-bold col-span-4 mx-auto">
                    {service.logo &&
                        <Image alt="service's logo" src={service.logo} width={200} height={200} className="rounded-xl w-[250px] h-[250px]"/>
                    }
                    <p className="text-center text-[60px] mb-[20px]">
                        {act?.name}
                    </p>
                    <p className="text-center text-[18px] mb-[20px]">
                        {act?.description}
                    </p>
                    {trigger ? (
                        <DisplayTrigger config={trigger.config_schema}/>
                    ) : (
                        "No trigger available"
                    )}
                </div>
            </div>
        </div>
    )
}

//-- Selectiong the action --//

function selectAct(setChoosingTrigger: (param: boolean) => void,
setAction: (param: Act | null) => void, act: Act)
{
    setChoosingTrigger(true);
    setAction(act);
}

//-- Choosing the action --//

interface ActionPageProp extends ChooseActProp
{
    type: string,
    service: Service,
    setService: (arg: Service | null) => void
}

function reinitAll(setService: (arg: any) => void, setAction: (arg: any) => void)
{
    setService(null);
    setAction(null);
}

function ChooseAct({service, setService, setAction,
    setChoosingAction, setConfig, type, act}: ActionPageProp)
{
    const [acts, setActs] = useState<Act[] | null>(null);
    const [choosingTrigger, setChoosingTrigger] = useState<boolean>(false);

    useEffect(() => {
        fetchActs(service.id, type, setActs);
    }, [])

    return (
        <div>
            {choosingTrigger && act ? (
                <ChooseTrigger act={act} type={type} service={service} setConfig={setConfig}
                setChoosingTrigger={setChoosingTrigger}/>
            ) : (
                <div>
                    <div className="grid grid-cols-4 text-white w-screen h-[450px] rounded-b-xl" style={{ background: service.color }}>
                        <Button className={`ml-[40px] mt-[40px] rounded-full border-${service.color} text-${service.color} hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[120px] text-[20px]`} onClick={() => reinitAll(setService, setAction)}>
                            Back
                        </Button>
                        <p className="mt-[35px] flex flex-col text-[50px] font-bold col-span-2 text-center">
                            Choose a trigger
                        </p>
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
                                <div key={act.id} className="rounded-xl w-[200px] h-[200px] hover:cursor-pointer relative" style={{ backgroundColor: service.color }} onClick={() => selectAct(setChoosingTrigger, setAction, act)}>
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
            )}
        </div>
    )
}

//-- Choosing the service --//

interface ChooseActProp
{
    type: string,
    act: Act | null,
    choosingAction: boolean,
    setAction: (arg: Act | null) => void,
    setChoosingAction: (data: boolean) => void,
    setConfig: (arg: ConfigRespAct | null) => void
}

function ChooseService({choosingAction, setChoosingAction,
    setConfig, setAction, type, act}: ChooseActProp)
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
                    <Services search={search} widgets={services} className="mt-[50px] grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-8 w-fit mx-auto" boxClassName="rounded-xl w-[200px] h-[200px] hover:cursor-pointer relative" onClick={setSelected}/>
                </div>
            }
            {selected &&
                <ChooseAct act={act} service={selected} setService={setSelected}
                choosingAction={choosingAction} setAction={setAction}
                setChoosingAction={setChoosingAction} type={type} setConfig={setConfig}/>
            }
        </div>
    )
}

//-- Main page choosing which page to display --//

export default function Create()
{
    const [action, setAction] = useState<Act | null>(null);
    const [reaction, setReaction] = useState<Act | null>(null);
    const [choosingAction, setChoosingAction] = useState(false);
    const [choosingReaction, setChoosingReaction] = useState(false);
    const [actConfig, setActConfig] = useState<ConfigRespAct | null>(null);
    const [reacConfig, setReacConfig] = useState<ConfigRespAct | null>(null);

    return (
        <div>
        {(!choosingAction && !choosingReaction) &&
            <Creation action={action} reaction={reaction}
            setChoosingReaction={setChoosingReaction}
            setChoosingAction={setChoosingAction}/>
        }
        {choosingAction &&
            <ChooseService act={action} setAction={setAction} type="actions"
            setConfig={setActConfig} choosingAction={choosingAction}
            setChoosingAction={setChoosingAction}
            />
        }
        {choosingReaction &&
            <ChooseService act={reaction} setAction={setReaction} type="reactions"
            choosingAction={choosingReaction} setConfig={setReacConfig}
            setChoosingAction={setChoosingReaction}
            />
        }
        </div>
    )
}
