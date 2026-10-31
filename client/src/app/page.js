import Link from 'next/link';
import ProductCard from '@/components/ProductCard';
import ProductImage from '@/components/ProductImage';
import HeroVideo from '@/components/HeroVideo';
import VideoPlayer from '@/components/VideoPlayer';
import JsonLd from '@/components/JsonLd';
import { products } from '@/lib/products';
import videos from '@/data/videos.json';
import { SITE } from '@/lib/site';

export const metadata = {
  title: { absolute: `${SITE.name} | ${SITE.tagline} Modern Sofas, Tables, Beds & Lighting` },
  description: 'Couchpuffy makes modern, puffy-comfortable furniture for living rooms, bedrooms and dining spaces. Free delivery over $500 and 30-day returns.',
  alternates: { canonical: '/' },
};

const categories = [
  { name: 'Sofas', slug: 'aurora-three-seater-sofa' },
  { name: 'Chairs', slug: 'halo-accent-chair' },
  { name: 'Tables', slug: 'meridian-dining-table' },
  { name: 'Beds', slug: 'haven-king-bed-frame' },
  { name: 'Storage', slug: 'atlas-open-bookshelf' },
  { name: 'Lighting', slug: 'lumen-floor-lamp' },
];

const perks = [
  { icon: '🚚', title: 'Free delivery', text: 'Complimentary delivery and assembly on orders over $500.' },
  { icon: '🌿', title: 'Sustainably made', text: 'FSC-certified wood and recycled fabrics in every collection.' },
  { icon: '🛡️', title: '10-year warranty', text: 'Built to last, with a decade of frame protection.' },
  { icon: '↩️', title: '30-day returns', text: 'Not in love with it? Send it back, no questions asked.' },
];

const reviews = [
  { name: 'Emily R.', text: 'The Aurora sofa transformed our living room. The quality is outstanding and delivery was effortless.' },
  { name: 'Marcus T.', text: 'Beautiful dining table, sturdy and elegant. Customer support helped me choose the perfect size.' },
  { name: 'Sofia L.', text: 'Fast shipping, easy assembly and the yellow finish looks stunning in our bedroom.' },
];

export default function HomePage() {
  const featured = products.filter((p) => p.badge === 'Best Seller' || p.badge === 'New').slice(0, 4);

  const videoSchema = videos.map((v) => ({
    '@context': 'https://schema.org',
    '@type': 'VideoObject',
    name: v.title,
    description: v.description,
    thumbnailUrl: `${SITE.url}${v.poster}`,
    contentUrl: `${SITE.url}${v.src}`,
    uploadDate: v.uploadDate,
    duration: v.iso,
  }));

  return (
    <>
      <JsonLd data={videoSchema} />

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-brand-50 to-white">
        <div className="container-x grid items-center gap-10 py-14 lg:grid-cols-2 lg:py-20">
          <div>
            <p className="eyebrow">New autumn collection</p>
            <h1 className="mt-4 text-4xl font-bold leading-tight sm:text-5xl lg:text-6xl">
              Level up your furniture with <span className="rounded-xl bg-brand-400 px-2">puffy</span> comfort.
            </h1>
            <p className="mt-6 max-w-xl text-lg text-stone-600">
              Soft shapes, honest materials and craftsmanship you can feel. Furnish your home with pieces made to be loved for decades.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link href="/products/" className="btn-primary">Shop collection</Link>
              <Link href="/contact/" className="btn-outline">Book a design consult</Link>
            </div>
            <dl className="mt-10 grid max-w-md grid-cols-3 gap-6 text-center sm:text-left">
              {[['12k+', 'Happy homes'], ['4.8★', 'Average rating'], ['10 yr', 'Warranty']].map(([v, l]) => (
                <div key={l}>
                  <dt className="font-display text-2xl font-bold">{v}</dt>
                  <dd className="text-sm text-stone-500">{l}</dd>
                </div>
              ))}
            </dl>
          </div>
          <HeroVideo src="/videos/hero-loop.mp4" poster="/images/video/hero-loop.webp" title="Couchpuffy furniture ad: level up your furniture" />
        </div>
      </section>

      {/* Categories */}
      <section className="section" aria-labelledby="cat-heading">
        <div className="container-x">
          <div className="text-center">
            <p className="eyebrow">Browse</p>
            <h2 id="cat-heading" className="mt-2 text-3xl font-bold sm:text-4xl">Shop by category</h2>
          </div>
          <ul className="mt-10 grid grid-cols-2 gap-5 md:grid-cols-3 lg:grid-cols-6">
            {categories.map((c) => (
              <li key={c.name}>
                <Link href="/products/" className="group block overflow-hidden rounded-2xl border border-stone-200 text-center transition hover:border-brand-400 hover:shadow-soft">
                  <div className="aspect-square overflow-hidden">
                    <ProductImage slug={c.slug} small alt={`${c.name} collection`} className="transition duration-500 group-hover:scale-105" />
                  </div>
                  <span className="block py-3 font-semibold group-hover:text-brand-600">{c.name}</span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Featured */}
      <section className="section bg-stone-50" aria-labelledby="feat-heading">
        <div className="container-x">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="eyebrow">Our favourites</p>
              <h2 id="feat-heading" className="mt-2 text-3xl font-bold sm:text-4xl">Featured furniture</h2>
            </div>
            <Link href="/products/" className="font-semibold text-brand-700 hover:underline">View all products →</Link>
          </div>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {featured.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </div>
      </section>

      {/* Ad videos */}
      <section className="section" aria-labelledby="video-heading">
        <div className="container-x">
          <div className="text-center">
            <p className="eyebrow">Watch</p>
            <h2 id="video-heading" className="mt-2 text-3xl font-bold sm:text-4xl">See Couchpuffy in action</h2>
            <p className="mx-auto mt-3 max-w-2xl text-stone-600">Short ads from our latest campaign. Press play to take a look inside our rooms.</p>
          </div>
          <div className="mt-10 grid gap-8 md:grid-cols-3">
            {videos.map((v) => (
              <figure key={v.id}>
                <VideoPlayer video={v} />
                <figcaption className="mt-3 text-sm font-medium text-stone-700">{v.title}</figcaption>
              </figure>
            ))}
          </div>
        </div>
      </section>

      {/* Perks */}
      <section className="section bg-stone-50" aria-labelledby="why-heading">
        <div className="container-x">
          <h2 id="why-heading" className="text-center text-3xl font-bold sm:text-4xl">Why choose Couchpuffy</h2>
          <ul className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {perks.map((p) => (
              <li key={p.title} className="rounded-2xl border border-stone-200 bg-white p-6 text-center">
                <span className="mx-auto grid h-14 w-14 place-items-center rounded-full bg-brand-100 text-2xl" aria-hidden="true">{p.icon}</span>
                <h3 className="mt-4 text-lg font-semibold">{p.title}</h3>
                <p className="mt-2 text-sm text-stone-600">{p.text}</p>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Testimonials */}
      <section className="section bg-brand-50" aria-labelledby="rev-heading">
        <div className="container-x">
          <h2 id="rev-heading" className="text-center text-3xl font-bold sm:text-4xl">Loved by our customers</h2>
          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {reviews.map((r) => (
              <figure key={r.name} className="rounded-2xl bg-white p-6 shadow-soft">
                <p className="text-brand-500" aria-label="5 out of 5 stars">★★★★★</p>
                <blockquote className="mt-3 text-stone-700">“{r.text}”</blockquote>
                <figcaption className="mt-4 text-sm font-semibold">{r.name}</figcaption>
              </figure>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section">
        <div className="container-x">
          <div className="rounded-3xl bg-brand-400 px-6 py-14 text-center sm:px-12">
            <h2 className="text-3xl font-bold sm:text-4xl">Let’s level up your space</h2>
            <p className="mx-auto mt-4 max-w-2xl text-ink/80">Talk to our interior specialists for a free consultation and a tailored furniture plan.</p>
            <Link href="/contact/" className="mt-8 inline-flex rounded-full bg-ink px-8 py-3 text-sm font-semibold text-white transition hover:bg-stone-800">
              Get free consultation
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
