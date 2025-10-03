/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** fetch
*/

export async function fetchServices(setServices: (data: any) => void)
{
    try {
        const res = await fetch("http://localhost:8080/services",
        {
            method: "GET",
            headers: { "Content-type": "application/json" },
        });

        if (!res.ok)
            return ("");
        const data = await res.json();
        setServices(data);
    } catch (err) {
        console.log("Error: ", err);
    }
}

export async function fetchApplets(setApplets: (data: any) => void)
{
    try {
        const res = await fetch("http://localhost:8080/areas",
        {
            method: "GET",
            headers: { "Content-type": "application/json" },
        });

        if (!res.ok)
            return ("");
        const data = await res.json();
        setApplets(data);
    } catch (err) {
        console.log("Error: ", err);
    }
}
