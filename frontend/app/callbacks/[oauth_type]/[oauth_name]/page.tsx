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
        window.location.href = `http://localhost:8080/oauth/login_oauth_token/${service}?code=${code}`
      } else if (oauth_type == "link") {
        window.location.href = `http://localhost:8080/oauth/oauth_token/${service}?code=${code}`
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
