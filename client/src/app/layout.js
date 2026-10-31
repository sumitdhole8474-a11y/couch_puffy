import './globals.css';
import { Inter, Playfair_Display } from 'next/font/google';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import JsonLd from '@/components/JsonLd';
import { SITE } from '@/lib/site';

const inter = Inter({ subsets: ['latin'], display: 'swap', variable: '--font-inter' });
const playfair = Playfair_Display({ subsets: ['latin'], display: 'swap', variable: '--font-playfair' });

export const metadata = {
  metadataBase: new URL(SITE.url),
  title: { default: `${SITE.name} | ${SITE.tagline}`, template: `%s | ${SITE.name}` },
  description: SITE.description,
  applicationName: SITE.name,
  keywords: ['couchpuffy', 'furniture', 'sofas', 'dining tables', 'beds', 'bookshelves', 'lamps', 'home decor', 'modern furniture'],
  authors: [{ name: SITE.name }],
  creator: SITE.name,
  openGraph: {
    type: 'website',
    siteName: SITE.name,
    locale: 'en_US',
    title: `${SITE.name} | ${SITE.tagline}`,
    description: SITE.description,
    images: [{ url: '/og-image.png', width: 1200, height: 630, alt: SITE.name }],
  },
  twitter: {
    card: 'summary_large_image',
    title: `${SITE.name} | ${SITE.tagline}`,
    description: SITE.description,
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, 'max-image-preview': 'large', 'max-snippet': -1 },
  },
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/favicon.svg', type: 'image/svg+xml' },
    ],
    apple: '/apple-touch-icon.png',
  },
};

export const viewport = { width: 'device-width', initialScale: 1, themeColor: '#FFC72C' };

const orgSchema = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'FurnitureStore',
      '@id': `${SITE.url}/#store`,
      name: SITE.name,
      url: SITE.url,
      telephone: SITE.phone,
      email: SITE.email,
      description: SITE.description,
      openingHours: 'Mo-Sa 09:00-19:00',
      address: { '@type': 'PostalAddress', streetAddress: '123 Maple Street', addressLocality: 'Portland', addressRegion: 'OR', postalCode: '97201', addressCountry: 'US' },
      logo: `${SITE.url}/icon-512.png`,
      image: `${SITE.url}/og-image.png`,
      sameAs: SITE.social,
    },
    { '@type': 'WebSite', '@id': `${SITE.url}/#website`, url: SITE.url, name: SITE.name, publisher: { '@id': `${SITE.url}/#store` } },
  ],
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <body>
        <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] focus:rounded-lg focus:bg-brand-400 focus:px-4 focus:py-2">
          Skip to content
        </a>
        <JsonLd data={orgSchema} />
        <Header />
        <main id="main">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
