/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import { fetchCreateApplet, fetchServices, fetchAction, fetchActs, fetchSpecificService } from "@/app/functions/fetch"
import { Service, Act, SpecificService, ActDetails } from "@/app/types/service"
import { ConfigRespAct, ConfigReqAct } from "@/app/types/config"
import ValidateButton from "@/app/components/Validation"
import Services from "@/app/components/Services"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { redirect } from "next/navigation"
import { SpecificAction, SpecificReaction } from "@/app/types/actions"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { fetchIsConnected } from "@/app/functions/fetch"
import { Checkbox } from "@/components/ui/checkbox"

//-- Buttons --//

interface ChoiceButtonProp {
  setIsChoosing: (data: boolean) => void,
  setChosen: (arg: ActDetails | null) => void,
  replacementText?: string,
  buttonText?: string,
  disable?: boolean,
  chosen: ActDetails | null,
  currentId: number,
  setCurrentId: (id: number) => void,
  setIsEditing: (editing: boolean) => void,
}

function ActionButton({ buttonText = "", replacementText = "", disable = false,
  setIsChoosing, setChosen, chosen, currentId, setCurrentId, setIsEditing }: ChoiceButtonProp) {
  return (
    <div className="mx-auto mt-[10%] w-[75%] h-[100px] md:h-[170px] rounded-xl text-white flex items-center" onClick={() => ""} style={{ background: (disable ? "grey" : "black") }}>
      <h1 className="flex-1 title inverted">
        {buttonText}
        {chosen ?
          <p className="ml-[20px] tiny-text inverted">{chosen.act.name.replaceAll("_", " ")}</p>
          :
          replacementText
        }
      </h1>
      {(!disable && !chosen) &&
        <Button className="mr-[20px] rounded-full text-black hover:bg-white bg-white hover:cursor-pointer px-[30px] py-[20px] font-bold w-[100px] text-[20px]" onClick={() => setIsChoosing(true)}>
          Add
        </Button>
      }
      {chosen &&
        <div>
          <button className="mr-[20px] mb-[5%] py-[5%] rounded-button w-[75%] font-bold" onClick={() => {setCurrentId(chosen.id); setIsChoosing(true); setIsEditing(true)}}>
            Edit
          </button>
          <button className="mr-[20px] py-[5%] rounded-button w-[75%] font-bold" onClick={() => setChosen(null)}>
            Delete
          </button>
        </div>
      }
    </div>
  )
}

interface UpButtonProp {
  text: string,
  act: (param: boolean | string) => void,
  param: boolean | string,
  color?: string
}

function LeftUpButton({ text, act, param, color = "black" }: UpButtonProp) {
  return (
    <Button className={`ml-[10%] mt-[20%] rounded-full border-${color} text-${color} hover:bg-transparent bg-transparent border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[120px] text-[20px]`} onClick={() => act(param)}>
      {text}
    </Button>
  )
}

//-- Send form --//

function createApplet(action: ActDetails, reactions: ActDetails[], title: string) {
    fetchCreateApplet(action, reactions, title);
    redirect("/my_applets");
}

//-- Creation page --//

interface CreationProps {
  theAction: ActDetails | null,
  setTheAction: (action: ActDetails | null) => void,
  theReactions: ActDetails[] | null,
  setTheReactions: (reactions: ActDetails[] | null) => void,
  setChoosingAction: (choosing: boolean) => void,
  setChoosingReaction: (choosing: boolean) => void,
  aReaction: ActDetails | null,
  currentId: number,
  setCurrentId: (id: number) => void,
  setIsEditing: (editing: boolean) => void,
}

function nextAvailableId(theReactions: ActDetails[], proposedId: number)
{
  let newId: number = proposedId;

  theReactions.map((reac) => {
    if (reac.id == proposedId)
      proposedId = proposedId + 1;
  });
  if (proposedId != newId)
    return nextAvailableId(theReactions, proposedId);
  return proposedId;
}

function Creation({ theAction, setTheAction, theReactions, setTheReactions, 
  setChoosingAction, setChoosingReaction, aReaction, currentId, setCurrentId,
  setIsEditing }: CreationProps)
{
  const [validating, setValidating] = useState<boolean>(false);
  const [title, setTitle] = useState<string>(`if ${theAction?.act.name}, then ${theReactions ? theReactions[0].act.name : ""}`);

  useEffect(() => {
    const checkingReactions = (newReac: ActDetails) => {
      if (!theReactions) {
        setTheReactions([newReac]);
        return;
      }
      const searched = theReactions.filter((insertedReac) =>
        newReac.id == insertedReac.id
      );
      if (searched.length == 0) {
        setTheReactions([...theReactions, newReac]);
        return;
      }
      const updatedReactions = theReactions.map((insertedReac) =>
        newReac.id == insertedReac.id ? newReac : insertedReac
      );
      setTheReactions(updatedReactions);
    };
    if (aReaction)
      checkingReactions(aReaction);
  }, [aReaction])

  const deleteReaction = (id: number) => {
    const newReactions = theReactions?.filter((reac) => reac.id != id);
    if (newReactions?.length == 0)
      setTheReactions(null);
    else
      setTheReactions(newReactions ? newReactions : null);
  }

  return (
    <div>
      {validating ? (
        <div>
          <div className="rounded-b-xl bg-black text-white font-bold w-screen h-[450px]">
            <div className="grid grid-cols-4">
              <LeftUpButton text="Back" act={(param: boolean | string) => setValidating(param as boolean)} param={false} color="white" />
              <p className="mt-[35px] flex flex-col text-[50px] col-span-2 text-center">
                Review and finish
              </p>
              <hr className="col-span-4 mb-[120px]" />
            </div>
            <p className="subtitle inverted centered mb-[20px]">Applet Title</p>
            <Input className="block mx-auto w-[75%] h-[10%] bg-white text-black" defaultValue={title} onChange={(e) => setTitle(e.target.value)} />
          </div>
          <div className="centered mt-[30px]">
            <button className="rounded-button inverted px-[5%] py-[3%]" onClick={() => createApplet(theAction as ActDetails, theReactions as ActDetails[], title)} disabled={title === "" || !theAction || !theReactions}>
              Finish
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="grid grid-cols-4">
            <LeftUpButton text="Cancel" act={(param: boolean | string) => redirect(param as string)} param={"/my_applets"} />
            <p className="mt-[35px] flex flex-col title col-span-2 text-center">
              Create
            </p>
          </div>
          <ActionButton buttonText="If " replacementText="This" setIsChoosing={setChoosingAction} setChosen={setTheAction} chosen={theAction} currentId={currentId} setCurrentId={setCurrentId} setIsEditing={setIsEditing} />
          {theReactions && theReactions.map((reac) => 
            <ActionButton key={reac.id} buttonText="Then " replacementText="That" disable={theAction == null} setIsChoosing={setChoosingReaction} setChosen={(_: ActDetails | null) => deleteReaction(reac.id)} chosen={reac} currentId={currentId} setCurrentId={setCurrentId} setIsEditing={setIsEditing} />
          )}
          {!theReactions &&
            <ActionButton buttonText="Then " replacementText="That" disable={theAction == null} setIsChoosing={setChoosingReaction} setChosen={() => ""} chosen={null} currentId={currentId} setCurrentId={setCurrentId} setIsEditing={setIsEditing}/>
          }
          {(theAction != null && theReactions != null) &&
            <div>
              <button className="mt-[5%] rounded-button inverted block mx-auto disabled:bg-gray-500" onClick={() => {setCurrentId(nextAvailableId(theReactions, 1)); setChoosingReaction(true)}}>
                +
              </button>
              <ValidateButton arg={true} clickAct={setValidating} text="Continue" addToClass={"mt-[100px] mb-[5%]"} inverted={true}/>
            </div>
          }
        </div>
      )}
    </div>
  )
}
// find a proper way to add or delete reactions
//-- Affichage des triggers --//

interface SelectElementProp {
  content: string[],
  config: ConfigReqAct,
  handleChange: (newTrigg: ConfigRespAct) => void
}

function defineChoice(val: string, setVal: (str: string) => void,
    handleChange: (newTrigg: ConfigRespAct) => void, config: ConfigReqAct)
{
    setVal(val);
    handleChange({
        name: config.name,
        type: config.type,
        values: val
    })
}

function SelectElement({ content, config, handleChange }: SelectElementProp) {

    const [val, setVal] = useState<string>(content[0]);
    const selectItemsBlock = content.map((value) =>
        <SelectItem key={value} value={value}>{value}</SelectItem>
    );

    return (
        <Select onValueChange={(v) => defineChoice(v, setVal, handleChange, config)}
            value={val}>
        <SelectTrigger className="w-[250px] text-black bg-white">
            <SelectValue placeholder={val} />
        </SelectTrigger>
        <SelectContent className="text-black">
            <SelectGroup>
            {selectItemsBlock}
            </SelectGroup>
        </SelectContent>
        </Select>
    )
}

function modifySelection(checkboxes : { [key: string]: boolean }[],
  config: ConfigReqAct, handleChange: (newTrigg: ConfigRespAct) => void)
{
  handleChange({
    name: config.name,
    type: config.type,
    values: checkboxes
  });
}

function CheckboxElement({ content, config, handleChange }: SelectElementProp)
{
  const initialBoxes: { [key: string]: boolean }[] = content.map((chk) => ({
    [chk]: false,
  }));

  const [checkboxes, setCheckboxes] = useState<{ [key: string]: boolean }[]>(initialBoxes);
  
  const handleChecking = (key: string, newValue: boolean) => {
    const updatedCheckboxes = checkboxes.map((item) =>
      key in item ? { [key]: newValue } : item
    );
    setCheckboxes(updatedCheckboxes);
    modifySelection(updatedCheckboxes, config, handleChange);
  };

  return (
    <div>
      {content.map((value) => {
        const checkbox = checkboxes.find((item) => value in item);
        const checked = checkbox ? checkbox[value] : false;

        return (<div className="flex items-center space-x-2" key={value}>
          <Checkbox
            id={value}
            checked={checked}
            onCheckedChange={() => handleChecking(value, !checked)}/>
          <label
            htmlFor={value}
            className="text-sm font-medium">
              {value}
          </label>
        </div>)
      })}
    </div>
  )
}

interface TriggerProp {
  config: ConfigReqAct,
  handleChange: (newTrigg: ConfigRespAct) => void
}

function DisplayTrigger({ config, handleChange }: TriggerProp)
{
    return (
        <div key={config.name}>
            <p className="mt-[20px] text-[20px] text-center">
                {config.name.replaceAll("_", " ")}
            </p>
            {(config.type == "select" && Array.isArray(config.values)
                && config.values.every(v => typeof v === "string")) &&
                <div className="centered">
                    <SelectElement content={config.values}
                    config={config} handleChange={handleChange}/>
                </div>
            }
            {config.type == "input" &&
                <Input onChange={(e) => defineChoice(e.target.value, () => "", handleChange, config)}/>
            }
            {(config.type == "check_list" && Array.isArray(config.values) && typeof config.values === "object") && 
                <CheckboxElement content={config.values}
                config={config} handleChange={handleChange}/>
            }
        </div>
    )
}

interface AllTriggerProp {
  config: ConfigReqAct[],
  configResp: ConfigRespAct[],
  setConfigResp: (arg: ConfigRespAct[]) => void
}

function DisplayAllTrigger({ config, configResp, setConfigResp }: AllTriggerProp)
{
    const handleTriggerChange = (newTrigg: ConfigRespAct) => {
      const updatedConfig = configResp.map(cfg =>
          cfg.name === newTrigg.name ? newTrigg : cfg
        );
        setConfigResp(updatedConfig);
    }

    return config.map((c) => {
        return <DisplayTrigger key={c.name} config={c} handleChange={handleTriggerChange}/>;
    })
}

//-- Choosing the trigger --//

interface chooseTriggerProp {
  type: string,
  actInfos: Act,
  service: Service,
  act: ActDetails | null,
  setIsChoosing: (data: boolean) => void,
  setActInfos: (arg: Act | null) => void,
  setAct: (arg: ActDetails | null) => void,
  setService: (arg: Service | null) => void,
  setChoosingTrigger: (arg: boolean) => void,
  currentId: number,
  isEditing: boolean,
  setIsEditing: (editing: boolean) => void,
}

interface reinitProp {
  setService: (arg: Service | null) => void,
  setAct: (arg: Act | null) => void
}

function reinitAll({setService, setAct}: reinitProp) {
    setService(null);
    setAct(null);
}

function unsetChoosingTime(actInfos: Act, configResp: ConfigRespAct[], setAct: (arg: ActDetails | null) => void,
  setActInfos: (arg: Act | null) => void, setService: (arg: Service | null) => void,
  setChoosingTrigger: (arg: boolean) => void, setIsChoosing: (arg: boolean) => void,
  setConfigResp: (arg: ConfigRespAct[]) => void, currentId: number,
  isEditing: boolean, setIsEditing: (editing: boolean) => void)
{
    const chosenAct : ActDetails = {
      id: currentId,
      act: actInfos,
      config: configResp,
    }
    setAct(chosenAct);
    setService(null);
    setActInfos(null);
    setConfigResp([]);
    setIsChoosing(false);
    setChoosingTrigger(false);
    if (isEditing)
      setIsEditing(false);
}

function allTriggersValid(configResp: ConfigRespAct[], configReq: ConfigReqAct[] | undefined)
{
  if (typeof configReq === "undefined")
    return false;
  if (configReq.length == 0)
    return true;
  if (configResp.length == 0)
    return false;

  const allValid = configResp.every(cfg => {
    if (cfg.type === "check_list")
      return Array.isArray(cfg.values) && cfg.values.length != 0;
    return (typeof cfg.values === "string" && cfg.values.trim() !== "");
  });

  return allValid;
}

function ChooseTrigger({ act, actInfos, service, type,
    setChoosingTrigger, setAct, setService, setIsChoosing, setActInfos,
    currentId, isEditing, setIsEditing }: chooseTriggerProp)
{
  const [trigger, setTrigger] = useState<SpecificAction | SpecificReaction | null>(null);
  const [configResp, setConfigResp] = useState<ConfigRespAct[]>([]);

  useEffect(() => {
    fetchAction(actInfos.id, type, setTrigger);
  }, []);

  useEffect(() => {
    if (trigger) {
      const initialConfig = trigger.config_schema.map(cfg => ({
        name: cfg.name,
        type: cfg.type,
        values: cfg.type === "check_list" ? [] : (cfg.type === "select" ? (typeof cfg.values[0] === "string" ? cfg.values[0] : "") : ""),
      }));
      setConfigResp(initialConfig);
    }
  }, [trigger]);

  return (
    <div className="text-white w-screen h-screen" style={{ background: service.color }}>
        <div className="grid grid-cols-4 " >
            <LeftUpButton text="Back" act={(param: boolean | string) => setChoosingTrigger(param as boolean)} param={false} color="white" />
            <p className="mt-[5%] title inverted col-span-4 mb-[10%]">
            Complete trigger fields
            </p>
            <hr className="col-span-4 mb-[20px]" />
            <div className="flex flex-col mb-[20px] font-bold col-span-4 mx-auto">
            <p className="title inverted mb-[20px]">
                {actInfos.name.replaceAll("_", " ")}
            </p>
            <p className="simple-text inverted centered mb-[20px]">
                {actInfos.description}
            </p>
            {trigger ? (
                <DisplayAllTrigger config={trigger.config_schema} configResp={configResp} setConfigResp={setConfigResp}/>
            ) : (
                "No trigger available"
            )}
            <Button className="rounded-full border-white text-white hover:bg-[#555555] bg-black border-[4px] hover:cursor-pointer px-[30px] py-[20px] font-bold w-[250px] h-[100px] text-[30px] mx-auto mt-[45px]" disabled={!allTriggersValid(configResp, trigger?.config_schema)} onClick={() => unsetChoosingTime(actInfos, configResp, setAct, setActInfos, setService, setChoosingTrigger, setIsChoosing, setConfigResp, currentId, isEditing, setIsEditing)}>
                Create trigger
            </Button>
        </div>
      </div>
    </div>
  )
}

//-- Choosing the action --//

interface ActionPageProp extends ChooseActProp {
  service: Service,
  setService: (arg: Service | null) => void,
  currentId: number,
  isEditing: boolean,
  setIsEditing: (editing: boolean) => void,
}

function ChooseAct({ service, setService, act, setAct, type, setIsChoosing,
  currentId, isEditing, setIsEditing }: ActionPageProp) {
  const [acts, setActs] = useState<Act[] | null>(null);
  const [actInfos, setActInfos] = useState<Act | null>(null);
  const [choosingTrigger, setChoosingTrigger] = useState<boolean>(false);

  useEffect(() => {
    const getActs = async() => {
      await fetchActs(service.id, type, setActs);
    }
    getActs();
  }, [])

  return (
    <div>
      {choosingTrigger && actInfos ? (
        <ChooseTrigger act={act} actInfos={actInfos} setActInfos={setActInfos} type={type} service={service} setAct={setAct}
          setChoosingTrigger={setChoosingTrigger} setIsChoosing={setIsChoosing} setService={setService} currentId={currentId} isEditing={isEditing} setIsEditing={setIsEditing}/>
      ) : (
        <div>
          <div className="grid grid-cols-4 text-white w-screen rounded-b-xl" style={{ background: service.color }}>
            <LeftUpButton text="Back" act={() => reinitAll({setService:setService, setAct:setActInfos})} param={true} color="white"/>
            <p className="mt-[30%] mb-[20%] title inverted col-span-2">
              Choose a trigger
            </p>
            <hr className="col-span-4" />
            <div className="flex flex-col justify-end text-[35px] mb-[20px] font-bold col-span-4 mx-auto">
              <p className="subtitle inverted mt-[10%]">{service.name}</p>
            </div>
          </div>
          {acts && acts.length > 0 ? (
            <div className=" w-[95%] mx-auto mt-[25px] grid xl:grid-cols-5 lg:grid-cols-4 grid-cols-3 gap-2">
              {acts.map((act) => (
                <div key={act.id} className="rounded-xl md:w-[250px] w-[150px] md:h-[250px] h-[150px] hover:cursor-pointer relative" style={{ backgroundColor: service.color }} onClick={() => {setActInfos(act); setChoosingTrigger(true);}}>
                  <div className="text-center pt-[5%]">
                    <p className="subtitle inverted m-[20px]">
                      {act.name.replaceAll("_", " ")}
                    </p>
                    <p className="simple-text inverted m-[20px] truncate">
                      {act.description.replaceAll("_", " ")}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="centered subtitle mt-[20px]">
              No {type} available for this service.
            </p>
          )}
        </div>
      )}
    </div>
  )
}

//-- Choosing the service --//

interface ChooseActProp {
  type: string,
  act: ActDetails | null,
  setIsChoosing: (arg: boolean) => void,
  setAct: (arg: ActDetails | null) => void,
}

interface ChooseServiceProps extends ChooseActProp {
  currentId: number,
  isEditing: boolean,
  setIsEditing: (editing: boolean) => void,
}

function ChooseService({ setIsChoosing, setAct, type, act,
  currentId, isEditing, setIsEditing }: ChooseServiceProps)
{
  const [search, setSearch] = useState<string>("");
  const [selected, setSelected] = useState<Service | null>(null);
  const [services, setServices] = useState<Service[] | null>(null);
  const [chosenService, setChosenService] = useState<SpecificService | null>(null);
  const [serviceConnected, setServiceConnected] = useState<boolean>(false);
  const [checkedConnection, setCheckedConnection] = useState<boolean>(false);

  useEffect(() => {
    fetchServices(setServices);
  }, [])

  useEffect(() => {
    if (!selected)
      return;
    const loadSpecificService = async () => {
      await fetchSpecificService(setChosenService, selected.id);
    }
    loadSpecificService();
  }, [selected])

  useEffect(() => {
    if (!chosenService)
      return;
    const checkServiceConnected = async () => {
      await fetchIsConnected(chosenService.id, setServiceConnected);
      setCheckedConnection(true);
    }
    checkServiceConnected();
  }, [chosenService]);

  useEffect(() => {
    if (!checkedConnection || !chosenService)
      return;
    console.log(chosenService)
    console.log(serviceConnected)
    console.log(chosenService?.oauth_required);
    if (!serviceConnected && chosenService.oauth_required)
      redirect(`/services/${chosenService.name}`);
    setCheckedConnection(false);
  }, [checkedConnection]);

  return (
    <div>
      {!selected &&
        <div>
          <div className="grid grid-cols-4">
            <LeftUpButton text="Back" act={(param: boolean | string) => {setIsChoosing(param as boolean); setIsEditing(false)}} param={false} />
            <p className="mt-[35px] flex flex-col text-[50px] font-bold col-span-2 text-center">
              Choose a service
            </p>
          </div>
          <Input className="w-[400px] mx-auto block mt-[50px] border-[4px] h-[50px] text-[20px] placeholder:text-[20px]" placeholder="Search services" onChange={(e) => setSearch(e.target.value)} />
          <Services search={search} services={services} className="mt-[50px] grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 w-fit mx-auto gap-[5px]" boxClassName="rounded-xl w-[200px] h-[200px] hover:cursor-pointer relative border-black border-[1px]" onClick={setSelected} />
        </div>
      }
      {((selected && serviceConnected && chosenService?.oauth_required) || (selected && chosenService && !chosenService.oauth_required)) &&
        <ChooseAct act={act} setAct={setAct} service={selected} setService={setSelected} setIsChoosing={setIsChoosing} type={type}
          currentId={currentId} isEditing={isEditing} setIsEditing={setIsEditing}/>
      }
    </div>
  )
}

//-- Main page choosing which page to display --//

export default function Create() {
  const [currentId, setCurrentId] = useState<number>(1);
  const [maxId, setMaxId] = useState<number>(1);
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [choosingAction, setChoosingAction] = useState(false);
  const [choosingReaction, setChoosingReaction] = useState(false);
  const [theAction, setTheAction] = useState<ActDetails | null>(null);
  const [aReaction, setAReaction] = useState<ActDetails | null>(null);
  const [theReactions, setTheReactions] = useState<ActDetails[] | null>(null);

  return (
    <div>
      {(!choosingAction && !choosingReaction) &&
        <Creation 
          theAction={theAction}
          setTheAction={setTheAction}
          theReactions={theReactions}
          setTheReactions={setTheReactions}
          setChoosingAction={setChoosingAction}
          setChoosingReaction={setChoosingReaction}
          aReaction={aReaction}
          currentId={currentId}
          setCurrentId={setCurrentId}
          setIsEditing={setIsEditing}
        />
      }
      {choosingAction &&
        <ChooseService 
          setIsChoosing={setChoosingAction} 
          act={theAction} 
          setAct={setTheAction}
          type="actions"
          currentId={currentId}
          isEditing={isEditing}
          setIsEditing={setIsEditing}
        />
      }
      {choosingReaction &&
        <ChooseService 
          setIsChoosing={setChoosingReaction} 
          act={aReaction} 
          setAct={setAReaction}
          type="reactions"
          currentId={currentId}
          isEditing={isEditing}
          setIsEditing={setIsEditing}
        />
      }
    </div>
  )
}