'use client';

import { useMemo, useState } from 'react';
import ProductCard from './ProductCard';

export default function ProductsGrid({ products, categories }) {
  const [category, setCategory] = useState('All');
  const [sort, setSort] = useState('featured');

  const list = useMemo(() => {
    const filtered = category === 'All' ? products : products.filter((p) => p.category === category);
    const sorted = [...filtered];
    if (sort === 'low') sorted.sort((a, b) => a.price - b.price);
    if (sort === 'high') sorted.sort((a, b) => b.price - a.price);
    if (sort === 'rating') sorted.sort((a, b) => b.rating - a.rating);
    return sorted;
  }, [products, category, sort]);

  return (
    <div>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap gap-2" role="group" aria-label="Filter by category">
          {categories.map((c) => (
            <button
              key={c}
              type="button"
              onClick={() => setCategory(c)}
              aria-pressed={category === c}
              className={`rounded-full border px-4 py-2 text-sm font-medium transition ${
                category === c ? 'border-brand-400 bg-brand-400 text-ink' : 'border-stone-200 bg-white hover:border-brand-400'
              }`}
            >
              {c}
            </button>
          ))}
        </div>
        <label className="flex items-center gap-2 text-sm">
          <span className="text-stone-600">Sort by</span>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            className="rounded-lg border border-stone-200 bg-white px-3 py-2"
          >
            <option value="featured">Featured</option>
            <option value="low">Price: low to high</option>
            <option value="high">Price: high to low</option>
            <option value="rating">Top rated</option>
          </select>
        </label>
      </div>

      <p className="mt-6 text-sm text-stone-500" aria-live="polite">{list.length} products</p>
      <div className="mt-4 grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {list.map((p) => <ProductCard key={p.id} product={p} />)}
      </div>
    </div>
  );
}
