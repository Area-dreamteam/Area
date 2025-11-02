/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

'use client'

import AppletManagement from "@/app/components/appletManagement";
import { ActDetails } from "@/app/types/service";
import { useState } from "react";

//-- Main page choosing which page to display --//

export default function Create() {
  const [theAction, setTheAction] = useState<ActDetails | null>(null);
  const [theReactions, setTheReactions] = useState<ActDetails[] | null>(null);

  return (
    <AppletManagement
      creating={true}
      theAction={theAction}
      setTheAction={setTheAction}
      theReactions={theReactions}
      setTheReactions={setTheReactions}
    />
  )
}