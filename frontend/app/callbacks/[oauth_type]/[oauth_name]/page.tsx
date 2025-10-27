'use client'
import { useSearchParams } from "next/navigation";
import { use, useEffect } from "react"

type CallbackProps = {
  params: Promise<{ oauth_type: string, oauth_name: string }>;
};

export default function Page({ params }: CallbackProps) {
  const searchParams = useSearchParams();
  const { oauth_name, oauth_type } = use(params);

  useEffect(() => {
    const code = searchParams.get("code");
    const state = searchParams.get("state");
    const service = oauth_name
    if (code) {
      let url = "";
      if (oauth_type == "login") {
        url = `/api/backend/oauth/login_oauth_token/${service}?code=${code}`
      } else if (oauth_type == "link") {
        url = `/api/backend/oauth/oauth_token/${service}?code=${code}`
      } else {
        console.error("unkown oauth method")
        return;
      }
      
      // Add state parameter if present
      if (state) {
        url += `&state=${state}`;
      }
      
      // For mobile flows, close the tab after a brief delay
      if (state === 'mobile') {
        setTimeout(() => {
          window.close();
        }, 100);
      }
      
      window.location.href = url;
    }
  }, [searchParams])

  return (
    <div>
      redirect page
    </div>
  )
}
