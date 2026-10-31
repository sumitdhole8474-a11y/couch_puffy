'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { NAV, SITE } from '@/lib/site';
import Logo from './Logo';

export default function Header() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname() || '/';

  const isActive = (href) => (href === '/' ? pathname === '/' : pathname.startsWith(href));

  return (
    <header className="sticky top-0 z-50 border-b border-stone-200 bg-white/90 backdrop-blur">
      <div className="bg-brand-400 py-1.5 text-center text-xs font-medium text-ink">
        Free delivery on orders over $500 · 30-day returns
      </div>
      <div className="container-x flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center" aria-label={`${SITE.name} home`}>
          <Logo variant="wordmark" className="h-9 w-auto" />
        </Link>

        <nav aria-label="Main" className="hidden items-center gap-8 md:flex">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              aria-current={isActive(item.href) ? 'page' : undefined}
              className={`text-sm font-medium transition hover:text-brand-600 ${
                isActive(item.href) ? 'text-brand-600' : 'text-stone-700'
              }`}
            >
              {item.label}
            </Link>
          ))}
          <Link href="/contact/" className="btn-primary !py-2">Get a quote</Link>
        </nav>

        <button
          type="button"
          className="rounded-md p-2 md:hidden"
          aria-expanded={open}
          aria-controls="mobile-menu"
          aria-label="Toggle menu"
          onClick={() => setOpen((v) => !v)}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
            {open ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
          </svg>
        </button>
      </div>

      {open && (
        <nav id="mobile-menu" aria-label="Mobile" className="border-t border-stone-200 bg-white md:hidden">
          <ul className="container-x flex flex-col py-3">
            {NAV.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  onClick={() => setOpen(false)}
                  className={`block rounded-lg px-3 py-3 font-medium ${isActive(item.href) ? 'bg-brand-50 text-brand-700' : ''}`}
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </header>
  );
}
