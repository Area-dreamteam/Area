import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/client.apk",
        destination: "/api/download/client",
      },
    ];
  },
  output: "standalone",
};

module.exports = nextConfig;
export default nextConfig;
