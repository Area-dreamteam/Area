/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** fetch
*/

import axios from 'axios'
import { Act } from '../types/service';

const Calls = axios.create({
  baseURL: "http://localhost:8080",
  withCredentials: true
})

export async function fetchLogin(email: string, password: string) {
  try {
    const res = await Calls.post("/auth/login", {
      email: email,
      password: password,
    });
    if (res.status != 200)
      return false;
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchRegister(email: string, password: string) {
  try {
    const res = await Calls.post("/auth/register", {
      name: email.split("@")[0],
      email: email,
      password: password,
    });

    if (res.status != 200)
      return false;
    return true;
  } catch (err) {
    console.log("An error occured: ", err)
  }
  return false;
}

export async function fetchActs(id: number, type: string, setActs: (data: any) => void) {
  try {
    const res = await Calls.get(`/services/${id}/${type}`);

    if (res.status != 200)
      return false;
    setActs(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchServices(setServices: (data: any) => void) {
  try {
    const res = await Calls.get("/services");

    if (res.status != 200) {
      setServices(null);
      return false;
    }
    setServices(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  setServices(null);
  return false;
}

export async function fetchSpecificService(setService: (data: any) => void, id: number) {
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

export async function fetchApplets(setApplets: (data: any) => void) {
  try {
    const res = await Calls.get("/areas/public");

    if (res.status != 200) {
      setApplets(null);
      return false;
    }
    setApplets(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  setApplets(null);
  return false
}

export async function fetchSpecificApplet(setApplet: (data: any) => void, id: number) {
  try {
    const res = await Calls.get(`/areas/public/${id}`);

    if (res.status != 200) {
      setApplet(null);
      return false;
    }
    setApplet(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  setApplet(null);
  return true;
}

export async function fetchAction(id: number, type: string, setAction: (data: any) => void) {
  try {
    const res = await Calls.get(`/${type}/${id}`);

    if (res.status != 200) {
      setAction(null);
      return false;
    }
    setAction(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  setAction(null);
  return true;
}

export async function fetchPersonalApplets(setPersonalApplets: (data: any) => void) {
  try {
    const res = await Calls.get("/areas/");

    if (res.status != 200) {
      setPersonalApplets(null);
      return;
    }
    setPersonalApplets(res.data);
  } catch (err) {
    console.log("Error: ", err);
  }
  setPersonalApplets(null);
}

export async function fetchCreateApplet(action: Act, reaction: Act, title: string) {
  try {
    const res = await Calls.post("/areas", {
      name: title,
      description: "",
      action: {
        action_id: action.id,
        config: ""
      },
      reaction: {
        reaction_id: reaction.id,
        config: ""
      }
    });

    if (res.status != 200) {
      return false;
    }
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}
