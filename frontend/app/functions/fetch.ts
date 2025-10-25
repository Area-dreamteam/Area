/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** fetch
 */

import axios from "axios";
import { Act, Service, SpecificService } from "../types/service";
import { MyProfileProp, UpdateProfileProp } from "../types/profile";
import { ConfigRespAct } from "../types/config";
import { PublicApplet, PrivateApplet, SpecificPublicApplet, SpecificPrivateApplet } from "../types/applet";
import { SpecificAction, SpecificReaction } from "../types/actions";

export const Calls = axios.create({
  baseURL: "/api/backend",
  withCredentials: true,
});

Calls.interceptors.response.use(
  (response) => response,
  (error) => {
    if (
      error.response &&
      (error.response.status === 401 || error.response.status === 403)
    ) {
      window.location.href = "/login";
    }

    return Promise.reject(error);
  },
);

export async function fetchDisconnectOauth(id: number) {
  try {
    const res = await Calls.delete(`/oauth/oauth_login/${id}/disconnect`);
    if (res.status != 200) {
      return false;
    }
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchMyself(setMyProfile: (arg: MyProfileProp | null) => void) {
  try {
    const res = await Calls.get("/users/me");
    if (res.status != 200) {
      setMyProfile(null);
      return false;
    }
    setMyProfile(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  setMyProfile(null);
  return false;
}

export async function fetchUpdateMyself(update: UpdateProfileProp, setMyProfile: (arg: MyProfileProp) => void)
{
  try {
    const res = await Calls.patch("/users/me",
    {
      name: update?.name,
      email: update?.email
    });
    if (res.status != 200) {
      return false;
    }
    setMyProfile(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchDeleteMyself() {
  try {
    const res = await Calls.delete("/users/me");
    if (res.status != 200) return false;
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchChangePassword(oldPassword: string, newPass: string)
{
  try {
    const res = await Calls.patch("/users/me/password",
    {
      password: oldPassword,
      newPass: newPass
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

export async function fetchLogin(email: string, password: string) {
  try {
    const res = await Calls.post("/auth/login", {
      email: email,
      password: password,
    });
    if (res.status != 200) return false;
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
    console.log(res);

    if (res.status != 200) return false;
    return true;
  } catch (err) {
    console.log("An error occured: ", err);
  }
  return false;
}

export async function fetchActs(
  id: number,
  type: string,
  setActs: (data: Act[]) => void,
) {
  try {
    const res = await Calls.get(`/services/${id}/${type}`);

    if (res.status != 200) return false;
    setActs(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchServices(setServices: (data: Service[] | null) => void) {
  try {
    const res = await Calls.get("/services/list");

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

export async function fetchSpecificService(
  setService: (data: SpecificService | null) => void,
  id: number,
) {
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

export async function fetchApplets(setApplets: (data: (PublicApplet | PrivateApplet)[] | null) => void) {
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
  return false;
}

export async function fetchSpecificApplet(
  setApplet: (data: SpecificPublicApplet | null) => void,
  id: number,
) {
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

export async function fetchDeletePersonalApplet(id: number) {
  try {
    const res = await Calls.delete(`/areas/${id}`);

    if (res.status != 200) {
      return false;
    }
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return true;
}

export async function fetchPrivateApplet(
  setApplet: (data: SpecificPrivateApplet | null) => void,
  id: number,
) {
  try {
    const res = await Calls.get(`/areas/${id}`);

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

export async function fetchAction(
  id: number,
  type: string,
  setAction: (data: SpecificAction | SpecificReaction | null) => void,
) {
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

export async function fetchPersonalApplets(
  setPersonalApplets: (data: (PrivateApplet)[] | null) => void,
) {
  try {
    const res = await Calls.get("/users/areas/me");

    if (res.status != 200) {
      setPersonalApplets(null);
      return false;
    }
    setPersonalApplets(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  setPersonalApplets(null);
  return false;
}

export async function fetchPersonalPublicApplets(
  setPersonalApplets: (data: (PrivateApplet)[] | null) => void,
) {
  try {
    const res = await Calls.get("/users/areas/public");

    if (res.status != 200) {
      setPersonalApplets(null);
      return false;
    }
    setPersonalApplets(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  setPersonalApplets(null);
  return false;
}

export async function fetchUnpublishPersonalApplet(id:number) {
  try {
    const res = await Calls.delete(`/users/areas/public/${id}/unpublish`);

    if (res.status != 200) {
      return false;
    }
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchPublishPersonalApplet(id:number) {
  try {
    const res = await Calls.post(`/users/areas/${id}/publish`);

    if (res.status != 200) {
      return false;
    }
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchPersonalAppletConnection(id:number, state: string) {
  try {
    const res = await Calls.patch(`/users/areas/${id}/${state}`);

    if (res.status != 200) {
      return false;
    }
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}

export async function fetchCreateApplet(
  action: Act,
  reaction: Act,
  title: string,
  actConfig: ConfigRespAct[],
  reactConfig: ConfigRespAct[],
) {
  try {
    const res = await Calls.post("/users/areas/me", {
      name: title.replaceAll("_", " "),
      description: "[description]",
      action: {
        action_id: action.id,
        config: actConfig,
      },
      reactions: [
        {
          reaction_id: reaction.id,
          config: reactConfig,
        },
      ],
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

export async function fetchIsConnected(id: number | string, setIsConnected: (data: boolean) => void)
{
  try {
    const res = await Calls.get(`/services/${id}/is_connected`);
    if (res.status != 200)
      return false;
    setIsConnected(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}
