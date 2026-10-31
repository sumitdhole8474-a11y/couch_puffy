/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',        // fully static site -> ./out
  trailingSlash: true,     // /about/index.html, friendly for any static host
  reactStrictMode: true,
  images: { unoptimized: true },
  compress: true,
};

export default nextConfig;
