# Couchpuffy Furniture – Next.js + Tailwind + Express + dotenv

A professional, static, SEO-ready furniture website (white & yellow theme) with dummy content.

## Stack
- **Next.js 14** (App Router, `output: 'export'` static site) + **Tailwind CSS**
- **Node.js + Express** API and static file server (helmet, compression, CORS, rate-limit)
- **dotenv** for configuration (`server/.env`, `client/.env.local`)

## Quick start
```bash
npm run install:all      # installs root, client and server dependencies
npm run dev              # client: http://localhost:3000 · API: http://localhost:5000
```

## Production (single server)
```bash
# set NEXT_PUBLIC_SITE_URL to your real domain in client/.env.local, and leave NEXT_PUBLIC_API_URL empty
npm run build            # exports static site to client/out
NODE_ENV=production npm start   # Express serves client/out + /api on PORT (default 5000)
```
You can also deploy `client/out` to any static host (Netlify, Vercel, S3/CloudFront) and the API separately.

## Environment variables
| File | Variable | Purpose |
|---|---|---|
| server/.env | `PORT`, `NODE_ENV`, `CLIENT_URL`, `STATIC_DIR`, `RATE_LIMIT_MAX` | server config |
| client/.env.local | `NEXT_PUBLIC_SITE_URL` | canonical URLs, sitemap, Open Graph |
| client/.env.local | `NEXT_PUBLIC_API_URL` | Express base URL (empty when same origin) |

## API
- `GET /api/health`
- `GET /api/products?category=Sofas`
- `GET /api/products/:slug`
- `POST /api/contact` `{ name, email, message }`

## SEO & performance included
- Per-page `<title>`, meta description, canonical URLs, Open Graph & Twitter cards
- JSON-LD: FurnitureStore, WebSite, Product (+ ratings/offers), BreadcrumbList, ItemList, ContactPage
- Auto-generated `sitemap.xml` and `robots.txt`
- Fully pre-rendered static HTML, `next/font` (no layout shift), inline SVG visuals (zero image requests)
- Semantic HTML, skip link, ARIA labels, reduced-motion support
- Long-term caching for `_next/static`, gzip via `compression`

## Customise
- Brand name, contact info: `client/src/lib/site.js`
- Products: `client/src/data/products.json` (mirror to `server/data/products.json`)
- Colours: `client/tailwind.config.js` (`brand` palette)
- Replace `public/og-image.png` (1200x630) and swap SVG visuals for real photos when ready.
