/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** Services
*/

import { ServiceSearchProp } from "../interface/search";

export default function Services({search = "", filter = null, services = null,
    className = "", boxClassName = "", onClick = () => ""}: ServiceSearchProp)
{
    if (services == null) {
        return (
            <p className="centered text-[20px] mt-[20px]">
                No service found.
            </p>
        )
    }
    const filteredServices = (filter ? services.filter(service =>
        service.category === filter
    ) : (
        services
    ));
    const searchedServices = filteredServices.filter(service =>
        service.name.toLowerCase().includes(search.toLowerCase())
    );
    const nbServices = searchedServices.length;
    const serviceBlocks = searchedServices.map((service) => ((
        <div key={service.id} className={boxClassName} style={{ backgroundColor: service.color }} onClick={() => onClick(service)}>
            {(service.image_url == "" || service.image_url == null) ? (
                ""
            ) : ( ""
                // <Image alt="service's logo" src={service.image_url} width={200} height={200} className="rounded-xl w-[200px] h-[200px]"/>
            )}
            <div className="centered bg-black rounded-t-lg">
                <p className="font-bold text-white text-[20px] m-[20px]">{service.name}</p>
            </div>
        </div>
    )))

    return (
        <div className="w-full">
            {nbServices != 0 ? (
                <div className={className}>
                    {serviceBlocks} 
                </div>
            ) : (
                <p className="centered text-[20px] mt-[20px]">
                    No service found.
                </p>
            )}
        </div>
    )
}
