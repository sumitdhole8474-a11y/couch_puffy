import Link from 'next/link';
import { notFound } from 'next/navigation';
import ProductImage from '@/components/ProductImage';
import ProductCard from '@/components/ProductCard';
import Stars from '@/components/Stars';
import JsonLd from '@/components/JsonLd';
import { products, getProduct, getRelated, formatPrice } from '@/lib/products';
import { SITE } from '@/lib/site';

export const dynamicParams = false;

export function generateStaticParams() {
  return products.map((p) => ({ slug: p.slug }));
}

export function generateMetadata({ params }) {
  const product = getProduct(params.slug);
  if (!product) return {};
  const title = `${product.name} – ${product.category}`;
  return {
    title,
    description: `${product.description} ${product.material}. From ${formatPrice(product.price)} with free delivery over $500.`,
    alternates: { canonical: `/products/${product.slug}/` },
    openGraph: { type: 'website', title, description: product.description, url: `/products/${product.slug}/`, images: [{ url: `/images/products/${product.slug}.webp`, width: 1200, height: 900, alt: product.name }] },
  };
}

export default function ProductPage({ params }) {
  const product = getProduct(params.slug);
  if (!product) notFound();
  const related = getRelated(product);
  const url = `${SITE.url}/products/${product.slug}/`;

  const schema = [
    {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: product.name,
      description: product.description,
      category: product.category,
      material: product.material,
      brand: { '@type': 'Brand', name: SITE.name },
      sku: `CP-${String(product.id).padStart(4, '0')}`,
      image: `${SITE.url}/images/products/${product.slug}.webp`,
      aggregateRating: { '@type': 'AggregateRating', ratingValue: product.rating, reviewCount: product.reviews },
      offers: {
        '@type': 'Offer',
        url,
        priceCurrency: 'USD',
        price: product.price,
        availability: 'https://schema.org/InStock',
        itemCondition: 'https://schema.org/NewCondition',
      },
    },
    {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: SITE.url },
        { '@type': 'ListItem', position: 2, name: 'Shop', item: `${SITE.url}/products/` },
        { '@type': 'ListItem', position: 3, name: product.name, item: url },
      ],
    },
  ];

  return (
    <>
      <JsonLd data={schema} />
      <div className="container-x py-8">
        <nav aria-label="Breadcrumb" className="text-sm text-stone-500">
          <ol className="flex flex-wrap gap-2">
            <li><Link href="/" className="hover:text-brand-600">Home</Link> /</li>
            <li><Link href="/products/" className="hover:text-brand-600">Shop</Link> /</li>
            <li aria-current="page" className="text-ink">{product.name}</li>
          </ol>
        </nav>

        <article className="mt-8 grid gap-10 lg:grid-cols-2">
          <div className="aspect-[4/3] overflow-hidden rounded-3xl border border-brand-200">
            <ProductImage slug={product.slug} priority sizes="(min-width: 1024px) 50vw, 100vw" alt={`${product.name} – ${product.category.toLowerCase()} by Couchpuffy`} />
          </div>

          <div>
            <p className="eyebrow">{product.category}</p>
            <h1 className="mt-2 text-3xl font-bold sm:text-4xl">{product.name}</h1>
            <div className="mt-3"><Stars rating={product.rating} reviews={product.reviews} /></div>

            <div className="mt-5 flex items-baseline gap-3">
              <span className="text-3xl font-bold">{formatPrice(product.price)}</span>
              {product.oldPrice && <span className="text-lg text-stone-400 line-through">{formatPrice(product.oldPrice)}</span>}
            </div>

            <p className="mt-5 text-stone-600">{product.description}</p>

            <ul className="mt-6 space-y-2">
              {product.features.map((f) => (
                <li key={f} className="flex gap-3 text-sm">
                  <span className="mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-full bg-brand-400 text-xs font-bold" aria-hidden="true">✓</span>
                  {f}
                </li>
              ))}
            </ul>

            <dl className="mt-6 grid grid-cols-2 gap-4 rounded-2xl bg-brand-50 p-5 text-sm">
              <div><dt className="text-stone-500">Dimensions (W x D x H)</dt><dd className="font-semibold">{product.dimensions}</dd></div>
              <div><dt className="text-stone-500">Material</dt><dd className="font-semibold">{product.material}</dd></div>
            </dl>

            <div className="mt-8 flex flex-wrap gap-4">
              <Link href="/contact/" className="btn-primary">Enquire about this item</Link>
              <Link href="/products/" className="btn-outline">Continue shopping</Link>
            </div>
          </div>
        </article>

        <section className="mt-20" aria-labelledby="related-heading">
          <h2 id="related-heading" className="text-2xl font-bold sm:text-3xl">You may also like</h2>
          <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {related.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>
      </div>
    </>
  );
}
