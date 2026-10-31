import Link from 'next/link';
import { NAV, SITE } from '@/lib/site';
import Logo from './Logo';

const categories = ['Sofas', 'Chairs', 'Tables', 'Beds', 'Storage', 'Lighting'];

export default function Footer() {
  return (
    <footer className="mt-20 bg-ink text-stone-300">
      <div className="container-x grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <Logo variant="dark" className="h-16 w-auto" />
          <p className="mt-5 text-sm leading-relaxed">{SITE.description}</p>
        </div>
        <div>
          <h2 className="font-sans text-sm font-semibold uppercase tracking-wider text-brand-400">Explore</h2>
          <ul className="mt-4 space-y-2 text-sm">
            {NAV.map((n) => (
              <li key={n.href}><Link href={n.href} className="hover:text-brand-300">{n.label}</Link></li>
            ))}
          </ul>
        </div>
        <div>
          <h2 className="font-sans text-sm font-semibold uppercase tracking-wider text-brand-400">Categories</h2>
          <ul className="mt-4 space-y-2 text-sm">
            {categories.map((c) => (
              <li key={c}><Link href="/products/" className="hover:text-brand-300">{c}</Link></li>
            ))}
          </ul>
        </div>
        <div>
          <h2 className="font-sans text-sm font-semibold uppercase tracking-wider text-brand-400">Visit us</h2>
          <address className="mt-4 space-y-2 text-sm not-italic">
            <p>{SITE.address}</p>
            <p><a href={`tel:${SITE.phone.replace(/[^+\d]/g, '')}`} className="hover:text-brand-300">{SITE.phone}</a></p>
            <p><a href={`mailto:${SITE.email}`} className="hover:text-brand-300">{SITE.email}</a></p>
            <p>{SITE.hours}</p>
          </address>
        </div>
      </div>
      <div className="border-t border-white/10 py-5 text-center text-xs text-stone-500">
        © {new Date().getFullYear()} {SITE.name}. All rights reserved. Demo website with dummy content.
      </div>
    </footer>
  );
}
