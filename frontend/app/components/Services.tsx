/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Services
*/

import Image from "next/image"
import { SearchProp } from "../interface/search";

export default function Services({search = "", widgets = null,
    className = "", boxClassName = "", onClick = () => ""}: SearchProp)
{
    if (widgets == null) {
        return (
            <p className="flex justify-center text-[20px] mt-[20px]">
                No service found.
            </p>
        )
    }

    const filteredServices = widgets.filter(service =>
        service.name.toLowerCase().includes(search.toLowerCase())
    );
    const nbServices = filteredServices.length;
    const serviceBlocks = widgets.map((service) => ((
        service.name.toLowerCase().includes(search.toLowerCase()) ?
        (
            <div key={service.id} className={boxClassName} style={{ backgroundColor: service.color }} onClick={() => onClick(service)}>
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
