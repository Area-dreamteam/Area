/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Applets
*/

import { AppletSearchProp } from "../interface/search";

export default function Applets({search = "", applets = null,
    className = "", boxClassName = "", onClick = () => ""}: AppletSearchProp)
{
    if (applets == null) {
        return (
            <p className="flex justify-center text-[20px] mt-[20px] mb-[20px]">
                No applet found.
            </p>
        )
    }
    const filteredServices = applets.filter(applet =>
        applet.name.toLowerCase().includes(search.toLowerCase())
    );
    const nbServices = filteredServices.length;
    const serviceBlocks = applets.map((applet) => ((
        applet.name.toLowerCase().includes(search.toLowerCase()) ?
        (
            <div key={applet.id} className={boxClassName} style={{ backgroundColor: applet.color }} onClick={() => onClick(applet)}>
                <div className="flex justify-center bg-black rounded-t-lg">
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
