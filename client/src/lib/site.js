export const SITE = {
  name: 'Couchpuffy',
  tagline: 'Level up your furniture!',
  description:
    'Couchpuffy makes puffy-comfortable sofas, chairs, dining tables, beds, storage and lighting. Level up your furniture with free delivery over $500.',
  url: (process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000').replace(/\/$/, ''),
  apiUrl: (process.env.NEXT_PUBLIC_API_URL || '').replace(/\/$/, ''),
  phone: '+1 (555) 010-2030',
  email: 'hello@couchpuffy.example',
  address: '123 Maple Street, Portland, OR 97201, USA',
  hours: 'Mon–Sat 9:00–19:00',
  social: ['https://facebook.com/', 'https://instagram.com/', 'https://pinterest.com/'],
};

export const NAV = [
  { href: '/', label: 'Home' },
  { href: '/products/', label: 'Shop' },
  { href: '/about/', label: 'About' },
  { href: '/contact/', label: 'Contact' },
];
