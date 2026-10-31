'use client';

import { useState } from 'react';
import { SITE } from '@/lib/site';

export default function ContactForm() {
  const [status, setStatus] = useState({ state: 'idle', message: '' });

  async function onSubmit(e) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = Object.fromEntries(new FormData(form));
    if (data.company) return; // honeypot
    setStatus({ state: 'loading', message: '' });
    try {
      const res = await fetch(`${SITE.apiUrl}/api/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: data.name, email: data.email, message: data.message }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.message || 'Something went wrong.');
      setStatus({ state: 'success', message: json.message });
      form.reset();
    } catch (err) {
      setStatus({ state: 'error', message: err.message || 'Could not send your message. Please try again.' });
    }
  }

  const field = 'mt-1 w-full rounded-xl border border-stone-300 bg-white px-4 py-3 text-sm placeholder:text-stone-400';

  return (
    <form onSubmit={onSubmit} className="space-y-5 rounded-2xl border border-stone-200 bg-white p-6 shadow-soft sm:p-8" noValidate>
      <div>
        <label htmlFor="name" className="text-sm font-medium">Full name</label>
        <input id="name" name="name" required minLength={2} autoComplete="name" className={field} placeholder="Jane Doe" />
      </div>
      <div>
        <label htmlFor="email" className="text-sm font-medium">Email</label>
        <input id="email" name="email" type="email" required autoComplete="email" className={field} placeholder="jane@example.com" />
      </div>
      <div>
        <label htmlFor="message" className="text-sm font-medium">How can we help?</label>
        <textarea id="message" name="message" required minLength={10} rows={5} className={field} placeholder="Tell us about the furniture you are looking for…" />
      </div>
      <input type="text" name="company" tabIndex={-1} autoComplete="off" className="hidden" aria-hidden="true" />
      <button type="submit" disabled={status.state === 'loading'} className="btn-primary w-full disabled:opacity-60">
        {status.state === 'loading' ? 'Sending…' : 'Send message'}
      </button>
      <p role="status" aria-live="polite" className={`text-sm ${status.state === 'error' ? 'text-red-600' : 'text-green-700'}`}>
        {status.message}
      </p>
    </form>
  );
}
