import Link from 'next/link';
import ProductImage from '@/components/ProductImage';
import { SITE } from '@/lib/site';

export const metadata = {
  title: 'About Us – Our Story & Craftsmanship',
  description: `Learn about ${SITE.name}: a family-run furniture studio creating sustainable, beautifully crafted pieces since 2009.`,
  alternates: { canonical: '/about/' },
};

const values = [
  { title: 'Craftsmanship', text: 'Every piece is built by skilled makers using time-tested joinery and quality control at every step.' },
  { title: 'Sustainability', text: 'We source FSC-certified timber, recycled textiles and low-impact finishes wherever possible.' },
  { title: 'Fair value', text: 'By designing and selling direct, we keep premium furniture accessible without cutting corners.' },
];

export default function AboutPage() {
  return (
    <>
      <section className="bg-brand-50 py-16">
        <div className="container-x grid items-center gap-10 lg:grid-cols-2">
          <div>
            <p className="eyebrow">Our story</p>
            <h1 className="mt-2 text-4xl font-bold sm:text-5xl">Making homes warmer since 2009</h1>
            <p className="mt-5 text-lg text-stone-600">
              Couchpuffy began in a small Portland workshop with one belief: great furniture should be beautiful, durable and kind to the planet. Today we furnish more than 12,000 homes.
            </p>
            <Link href="/products/" className="btn-primary mt-8">Explore the collection</Link>
          </div>
          <div className="aspect-[4/3] overflow-hidden rounded-3xl border border-brand-200">
            <ProductImage slug="meridian-dining-table" priority sizes="(min-width: 1024px) 50vw, 100vw" alt="Handcrafted Meridian dining table in a bright Couchpuffy showroom" />
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container-x">
          <h2 className="text-center text-3xl font-bold sm:text-4xl">What we stand for</h2>
          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {values.map((v) => (
              <div key={v.title} className="rounded-2xl border border-stone-200 p-8">
                <div className="h-1.5 w-12 rounded-full bg-brand-400" />
                <h3 className="mt-5 text-xl font-semibold">{v.title}</h3>
                <p className="mt-3 text-stone-600">{v.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-ink py-14 text-white">
        <dl className="container-x grid grid-cols-2 gap-8 text-center md:grid-cols-4">
          {[['15+', 'Years of craft'], ['12k+', 'Homes furnished'], ['60', 'Skilled makers'], ['98%', 'Customer satisfaction']].map(([v, l]) => (
            <div key={l}>
              <dt className="font-display text-4xl font-bold text-brand-400">{v}</dt>
              <dd className="mt-1 text-sm text-stone-300">{l}</dd>
            </div>
          ))}
        </dl>
      </section>
    </>
  );
}
