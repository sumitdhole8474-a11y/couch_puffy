require('dotenv').config();

const path = require('path');
const fs = require('fs');
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

const products = require('./data/products.json');

const app = express();
const PORT = Number(process.env.PORT) || 5000;
const isProd = process.env.NODE_ENV === 'production';
const STATIC_DIR = path.resolve(__dirname, process.env.STATIC_DIR || '../client/out');

/* ---------- Security & performance middleware ---------- */
app.disable('x-powered-by');
app.use(helmet({ contentSecurityPolicy: false })); // Next.js static export uses inline scripts
app.use(compression());
app.use(
  cors({
    origin: (process.env.CLIENT_URL || 'http://localhost:3000').split(',').map((s) => s.trim()),
    methods: ['GET', 'POST'],
  })
);
app.use(express.json({ limit: '10kb' }));
if (!isProd) app.use(morgan('dev'));

app.use(
  '/api',
  rateLimit({
    windowMs: 15 * 60 * 1000,
    max: Number(process.env.RATE_LIMIT_MAX) || 100,
    standardHeaders: true,
    legacyHeaders: false,
  })
);

/* ---------- API routes ---------- */
app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.get('/api/products', (req, res) => {
  const { category } = req.query;
  const list = category
    ? products.filter((p) => p.category.toLowerCase() === String(category).toLowerCase())
    : products;
  res.set('Cache-Control', 'public, max-age=300');
  res.json({ count: list.length, products: list });
});

app.get('/api/products/:slug', (req, res) => {
  const product = products.find((p) => p.slug === req.params.slug);
  if (!product) return res.status(404).json({ message: 'Product not found' });
  res.set('Cache-Control', 'public, max-age=300');
  res.json(product);
});

app.post('/api/contact', (req, res) => {
  const { name, email, message } = req.body || {};
  const emailOk = typeof email === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  if (!name || String(name).trim().length < 2 || !emailOk || !message || String(message).trim().length < 10) {
    return res.status(400).json({ message: 'Please provide a valid name, email and a message (min 10 characters).' });
  }
  // Demo only: plug in Nodemailer / a CRM here. Never log real personal data in production.
  console.log(`[contact] New enquiry from ${String(name).trim()}`);
  res.status(201).json({ message: 'Thank you! Our team will get back to you within one business day.' });
});

app.use('/api', (_req, res) => res.status(404).json({ message: 'Not found' }));

/* ---------- Serve the static Next.js export (production) ---------- */
if (fs.existsSync(STATIC_DIR)) {
  app.use(
    express.static(STATIC_DIR, {
      extensions: ['html'],
      setHeaders(res, filePath) {
        if (filePath.includes(`${path.sep}_next${path.sep}static${path.sep}`)) {
          res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
        } else if (/\.(webp|png|jpe?g|svg|ico|mp4|webm)$/i.test(filePath)) {
          res.setHeader('Cache-Control', 'public, max-age=604800'); // images, logo and ad videos: 7 days
        } else if (filePath.endsWith('.html')) {
          res.setHeader('Cache-Control', 'public, max-age=0, must-revalidate');
        } else {
          res.setHeader('Cache-Control', 'public, max-age=86400');
        }
      },
    })
  );
  app.use((_req, res) => res.status(404).sendFile(path.join(STATIC_DIR, '404.html')));
} else {
  app.get('/', (_req, res) =>
    res.send('API running. Build the client (npm run build) to serve the website from this server.')
  );
}

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT} (${process.env.NODE_ENV || 'development'})`);
});
