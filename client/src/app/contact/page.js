import ContactForm from '@/components/ContactForm';
import JsonLd from '@/components/JsonLd';
import { SITE } from '@/lib/site';

export const metadata = {
  title: 'Contact Us – Free Design Consultation',
  description: `Get in touch with ${SITE.name} for product advice, quotes or a free interior design consultation. We reply within one business day.`,
  alternates: { canonical: '/contact/' },
};

export default function ContactPage() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'ContactPage',
    name: 'Contact Couchpuffy',
    url: `${SITE.url}/contact/`,
  };

  return (
    <>
      <JsonLd data={schema} />
      <section className="bg-brand-50 py-14">
        <div className="container-x">
          <p className="eyebrow">Contact</p>
          <h1 className="mt-2 text-4xl font-bold sm:text-5xl">We’d love to hear from you</h1>
          <p className="mt-3 max-w-2xl text-stone-600">Questions, quotes or styling advice? Send us a message and our team will reply within one business day.</p>
        </div>
      </section>
      <section className="container-x grid gap-10 py-14 lg:grid-cols-5">
        <div className="lg:col-span-3"><ContactForm /></div>
        <aside className="space-y-6 lg:col-span-2" aria-label="Store information">
          {[
            ['Showroom', SITE.address],
            ['Phone', SITE.phone],
            ['Email', SITE.email],
            ['Opening hours', SITE.hours],
          ].map(([t, v]) => (
            <div key={t} className="rounded-2xl border border-stone-200 p-5">
              <h2 className="font-sans text-sm font-semibold uppercase tracking-wider text-brand-600">{t}</h2>
              <p className="mt-1">{v}</p>
            </div>
          ))}
        </aside>
      </section>
    </>
  );
}
