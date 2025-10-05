/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** fetch
*/

import axios from 'axios'

const Calls = axios.create({
    baseURL: "http://localhost:8080",
    withCredentials: true
})

export async function fetchLogin(email: string, password: string)
{
    try {
        const res = await Calls.post("/auth/login", {
            // name: "",
            email: email,
            password: password,
            // role: "user"
        });
        if (res.status != 200)
            return false;
        return true;
    } catch (err) {
        console.log("Error: ", err);
    }
    return false;
}

export async function fetchRegister(email: string, password: string)
{
    try {
        const res = await Calls.post("/auth/register", {
            name: email.split("@")[0],
            email: email,
            password: password,
            // role: "user"
        });

        if (res.status != 200)
            return false;
        return true;
    } catch (err) {
        console.log("An error occured: ", err)
    }
    return false;
}

export async function fetchServices(setServices: (data: any) => void)
{
    try {
        const res = await Calls.get("/services");

        if (res.status != 200)
            return false;
        setServices(res.data);
        return true;
    } catch (err) {
        console.log("Error: ", err);
    }
    return false;
}

export async function fetchSpecificService(setService: (data: any) => void, id: number)
{
    try {
        const res = await Calls.get(`/services/${id}`);

        if (res.status != 200) {
            setService(null);
            return false;
        }
        setService(res.data);
        return true;
    } catch (err) {
        console.log("Error: ", err);
    }
    setService(null);
    return true;
}

export async function fetchApplets(setApplets: (data: any) => void)
{
    try {
        const res = await Calls.get("/areas/public");

        if (res.status != 200)
            return;
        setApplets(res.data);
    } catch (err) {
        console.log("Error: ", err);
    }
}
