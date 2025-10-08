'use client'
import { useSearchParams } from "next/navigation";
import { useEffect } from "react"

export default function Page() {
  const searchParams = useSearchParams();

  useEffect(() => {
    const code = searchParams.get("code");
    if (code) {
      window.location.href = `http://localhost:8080/services/todoist/login_oauth_token?code=${code}`
    }
  }, [searchParams])

  return (
    <div>
      redirect page
    </div>
  )
}
