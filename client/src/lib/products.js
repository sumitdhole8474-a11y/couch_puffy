import data from '@/data/products.json';

export const products = data;
export const categories = ['All', ...Array.from(new Set(data.map((p) => p.category)))];

export const getProduct = (slug) => data.find((p) => p.slug === slug);
export const getRelated = (product, limit = 4) =>
  data.filter((p) => p.category === product.category && p.id !== product.id)
    .concat(data.filter((p) => p.category !== product.category && p.id !== product.id))
    .slice(0, limit);

export const formatPrice = (n) => `$${n.toLocaleString('en-US')}`;

export const productImage = (p) => `/images/products/${p.slug}.webp`;
