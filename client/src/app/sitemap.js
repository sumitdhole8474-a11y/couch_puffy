import { products } from '@/lib/products';
import { SITE } from '@/lib/site';

export const dynamic = 'force-static';

export default function sitemap() {
  const now = new Date();
  const pages = ['/', '/products/', '/about/', '/contact/'].map((p) => ({
    url: `${SITE.url}${p}`,
    lastModified: now,
    changeFrequency: p === '/' ? 'weekly' : 'monthly',
    priority: p === '/' ? 1 : 0.8,
  }));
  const items = products.map((p) => ({
    url: `${SITE.url}/products/${p.slug}/`,
    lastModified: now,
    changeFrequency: 'monthly',
    priority: 0.7,
  }));
  return [...pages, ...items];
}
