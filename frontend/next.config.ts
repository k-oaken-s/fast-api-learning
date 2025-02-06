import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    domains: ['storage.googleapis.com'], // Google Cloud Storageのドメインを許可
  },
  // バックエンドAPIのプロキシ設定
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
};

export default nextConfig;
