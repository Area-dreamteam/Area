/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Applets
*/

import Image from "next/image"
import { SearchProp } from "../interface/search";

export default function Applets({search = "", widgets = null,
    className = "", boxClassName = "", onClick = () => ""}: SearchProp)
{
    if (widgets == null) {
        return (
            <p className="flex justify-center text-[20px] mt-[20px] mb-[20px]">
                No applet found.
            </p>
        )
    }

    const filteredServices = widgets.filter(applet =>
        applet.name.toLowerCase().includes(search.toLowerCase())
    );
    const nbServices = filteredServices.length;
    const serviceBlocks = widgets.map((applet) => ((
        applet.name.toLowerCase().includes(search.toLowerCase()) ?
        (
            <div key={applet.id} className={boxClassName} style={{ backgroundColor: applet.color }} onClick={() => onClick(applet)}>
                { applet.logo == "" || applet.logo == null ? "" : (<Image alt="applet's logo" src={applet.logo} width={200} height={200} className="rounded-xl w-[200px] h-[200px]"/>)}
                <div className="flex justify-center">
                    <p className="font-bold text-white text-[20px] m-[20px]">{applet.name}</p>
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
                    No applet found.
                </p>
            )}
        </div>
    )
}
