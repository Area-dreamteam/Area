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
    const service = oauth_name
    if (code) {
      if (oauth_type == "login") {
        window.location.href = `/api/backend/oauth/login_oauth_token/${service}?code=${code}`
      } else if (oauth_type == "link") {
        window.location.href = `/api/backend/oauth/oauth_token/${service}?code=${code}`
      } else {
        console.error("unkown oauth method")
      }
    }
  }, [searchParams])

  return (
    <div>
      redirect page
    </div>
  )
}
