import Link from 'next/link';
import ProductImage from './ProductImage';
import Stars from './Stars';
import { formatPrice } from '@/lib/products';

export default function ProductCard({ product }) {
  return (
    <article className="group flex flex-col overflow-hidden rounded-2xl border border-stone-200 bg-white transition hover:-translate-y-1 hover:shadow-soft">
      <Link href={`/products/${product.slug}/`} className="relative block aspect-[4/3] overflow-hidden" aria-label={`View ${product.name}`}>
        <ProductImage slug={product.slug} alt={`${product.name} – ${product.category.toLowerCase()} by Couchpuffy`} className="transition duration-500 group-hover:scale-105" />
        {product.badge && (
          <span className="absolute left-3 top-3 rounded-full bg-brand-400 px-3 py-1 text-xs font-bold text-ink">{product.badge}</span>
        )}
      </Link>
      <div className="flex flex-1 flex-col gap-2 p-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-brand-600">{product.category}</p>
        <h3 className="text-lg font-semibold leading-snug">
          <Link href={`/products/${product.slug}/`} className="hover:text-brand-600">{product.name}</Link>
        </h3>
        <Stars rating={product.rating} reviews={product.reviews} />
        <div className="mt-auto flex items-baseline gap-2 pt-2">
          <span className="text-xl font-bold">{formatPrice(product.price)}</span>
          {product.oldPrice && <span className="text-sm text-stone-400 line-through">{formatPrice(product.oldPrice)}</span>}
        </div>
      </div>
    </article>
  );
}
