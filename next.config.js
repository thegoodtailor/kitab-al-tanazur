/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  basePath: process.env.NODE_ENV === 'production' ? '/kitab-al-tanazur' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/kitab-al-tanazur/' : '',
  trailingSlash: true,
}

module.exports = nextConfig
