// Responsive, lazy-loaded product / scene image (WebP, 600w + 1200w).
export default function ProductImage({
  slug,
  alt,
  priority = false,
  small = false,
  sizes = '(min-width: 1280px) 25vw, (min-width: 640px) 50vw, 100vw',
  className = '',
}) {
  const base = `/images/products/${slug}`;
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={small ? `${base}-sm.webp` : `${base}.webp`}
      srcSet={small ? undefined : `${base}-sm.webp 600w, ${base}.webp 1200w`}
      sizes={small ? undefined : sizes}
      width={small ? 600 : 1200}
      height={small ? 450 : 900}
      alt={alt}
      loading={priority ? 'eager' : 'lazy'}
      decoding="async"
      fetchPriority={priority ? 'high' : undefined}
      className={`h-full w-full object-cover ${className}`}
    />
  );
}
