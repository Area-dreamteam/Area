import { useEffect, useState } from "react";
import { Calls } from "./fetch";

export interface UserInfos {
  id: number;
  name: string;
  email: string;
  role: string;
}

export function useAuth() {
  const [user, setUser] = useState<UserInfos | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await Calls.get("/users/me");

        if (res.status != 200) {
          setUser(null);
        } else {
          const data = await res.data;
          setUser(data);
        }
      } catch (err) {
        console.error("Auth check failed:", err);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  return { user, loading };
}
