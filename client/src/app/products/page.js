import ProductsGrid from '@/components/ProductsGrid';
import JsonLd from '@/components/JsonLd';
import { products, categories } from '@/lib/products';
import { SITE } from '@/lib/site';

export const metadata = {
  title: 'Shop Furniture – Sofas, Chairs, Tables, Beds & More',
  description: 'Browse our full furniture collection: sofas, accent chairs, dining tables, beds, storage and lighting. Free delivery over $500.',
  alternates: { canonical: '/products/' },
};

export default function ProductsPage() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    itemListElement: products.map((p, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      url: `${SITE.url}/products/${p.slug}/`,
      name: p.name,
    })),
  };

  return (
    <>
      <JsonLd data={schema} />
      <section className="bg-brand-50 py-14">
        <div className="container-x">
          <p className="eyebrow">Shop</p>
          <h1 className="mt-2 text-4xl font-bold sm:text-5xl">All furniture</h1>
          <p className="mt-3 max-w-2xl text-stone-600">Premium pieces for every room, designed to last and made to be loved.</p>
        </div>
      </section>
      <section className="container-x py-12">
        <ProductsGrid products={products} categories={categories} />
      </section>
    </>
  );
}
