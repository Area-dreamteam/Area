import { Calls } from "./fetch";

const handleOauthLogin = (service: string, destination: string) => {
  const authWindow = window.open(
    `http://localhost:8080/services/${service}/index`,
    "GitHub Login",
    "width=600,height=700",
  );

  window.addEventListener("message", (event) => {
    if (event.data.type === `${service}_login_complete`) {
      console.log(`${service} login finished. Cookie should now be set.`);
      window.location.href = destination;
    }
  });
};

const handleOauthAddService = (
  service: string,
  destination: string,
  id: number | string,
) => {
  const authWindow = window.open(
    `http://localhost:8080/services/${service}/index/${id}`,
    "GitHub Login",
    "width=600,height=700",
  );

  window.addEventListener("message", (event) => {
    if (event.data.type === `${service}_login_complete`) {
      console.log(`${service} login finished. Cookie should now be set.`);
      window.location.href = destination;
    }
  });
};

export async function redirectOauth(
  service: string,
  destination: string = "/explore",
) {
  try {
    handleOauthLogin(service, destination);
  } catch (err) {
    console.log("Error: ", err);
  }
}

export async function redirectOauthAddService(
  service: string,
  id: number | string,
  destination: string = "/explore",
) {
  try {
    handleOauthAddService(service, destination, id);
  } catch (err) {
    console.log("Error: ", err);
  }
}

export async function fetchIsConnected(
  id: number | string,
  setIsConnected: (data: boolean) => void,
) {
  try {
    const res = await Calls.get(`/services/${id}/is_connected`);

    if (res.status != 200) return false;
    setIsConnected(res.data);
    return true;
  } catch (err) {
    console.log("Error: ", err);
  }
  return false;
}
