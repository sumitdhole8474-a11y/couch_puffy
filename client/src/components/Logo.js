// Redesigned Couchpuffy logo (SVG, text converted to outlines so it renders identically everywhere).
const FILES = {
  wordmark: ['/logo-wordmark.svg', 345, 72],
  full: ['/logo.svg', 345, 106],
  dark: ['/logo-dark.svg', 345, 106],
};

export default function Logo({ variant = 'wordmark', className = 'h-9 w-auto' }) {
  const [src, width, height] = FILES[variant];
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img src={src} width={width} height={height} alt="Couchpuffy – level up your furniture!" className={className} decoding="async" />
  );
}
