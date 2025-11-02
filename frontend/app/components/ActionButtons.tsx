/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** ActionButtons
*/

import { Button } from "@/components/ui/button";
import { ActDetails } from "../types/service";


interface ChoiceButtonProp {
    setIsChoosing: (data: boolean) => void,
    setChosen: (arg: ActDetails | null) => void,
    replacementText?: string,
    buttonText?: string,
    disable?: boolean,
    chosen: ActDetails | null,
    setCurrentId: (id: number) => void,
    setIsEditing: (editing: boolean) => void,
  }

export function ActionButton({ buttonText = "", replacementText = "", disable = false,
  setIsChoosing, setChosen, chosen, setCurrentId, setIsEditing }: ChoiceButtonProp) {
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
        <Button aria-label="You can add an action or reaction by clicking here" className="mr-[20px] rounded-full text-black hover:bg-white bg-white hover:cursor-pointer px-[30px] py-[20px] font-bold w-[100px] text-[20px]" onClick={() => setIsChoosing(true)}>
          Add
        </Button>
      }
      {chosen &&
        <div>
          <button aria-label="You can change your selected action or reaction by clicking here" className="mr-[20px] mb-[5%] py-[5%] rounded-button w-[75%] font-bold" onClick={() => {setCurrentId(chosen.id); setIsChoosing(true); setIsEditing(true)}}>
            Edit
          </button>
          <button aria-label="You can delete your selected action or reaction by clicking here" className="mr-[20px] py-[5%] rounded-button w-[75%] font-bold" onClick={() => setChosen(null)}>
            Delete
          </button>
        </div>
      }
    </div>
  )
}
