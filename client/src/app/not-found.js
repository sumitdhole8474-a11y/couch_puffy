import Link from 'next/link';

export const metadata = { title: 'Page not found', robots: { index: false } };

export default function NotFound() {
  return (
    <section className="container-x py-24 text-center">
      <p className="eyebrow">404</p>
      <h1 className="mt-2 text-4xl font-bold">We couldn’t find that page</h1>
      <p className="mt-3 text-stone-600">The page may have moved. Let’s get you back to the furniture.</p>
      <Link href="/products/" className="btn-primary mt-8">Browse products</Link>
    </section>
  );
}
