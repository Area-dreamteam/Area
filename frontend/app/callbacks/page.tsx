'use client'
import { useSearchParams } from "next/navigation";
import { useEffect } from "react"

export default function Page() {
  const searchParams = useSearchParams();

  useEffect(() => {
    const code = searchParams.get("code");
    const service = searchParams.get("service");
    if (code) {
      window.location.href = `http://localhost:8080/services/todoist/login_oauth_token${service}/?code=${code}`
    }
  }, [searchParams])

  return (
    <div>
      redirect page
    </div>
  )
}
