/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** fetch
*/

import axios from 'axios'
import getCookies from './cookies';

const Calls = axios.create({
    baseURL: "http://localhost:8080",
    withCredentials: true
})

Calls.interceptors.request.use(
    (config) => {
      const token = getCookies('access_token');
      
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

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
            return;
        setServices(res.data);
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
