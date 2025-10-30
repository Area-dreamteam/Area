import type { NextConfig } from 'next'

const API_URL = process.env.BACKEND_URL || 'https://area-prod-back.onrender.com'

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: `${API_URL}/:path*`,
      },
      {
        source: '/about.json',
        destination: `${API_URL}/about.json`,
      },
    ]
  },
  output: 'standalone',
  allowedDevOrigins: ['local-origin.dev', '*.local-origin.dev'],
}

module.exports = nextConfig
export default nextConfig
