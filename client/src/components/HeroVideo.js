'use client';

import { useEffect, useRef, useState } from 'react';

// Muted looping ad. Respects prefers-reduced-motion and has a pause control (WCAG 2.2.2).
export default function HeroVideo({ src, poster, title }) {
  const ref = useRef(null);
  const [reduced, setReduced] = useState(false);
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    setReduced(window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }, []);

  function toggle() {
    const v = ref.current;
    if (!v) return;
    if (v.paused) { v.play(); setPaused(false); } else { v.pause(); setPaused(true); }
  }

  return (
    <div className="relative aspect-video w-full overflow-hidden rounded-3xl border border-brand-200 bg-brand-50 shadow-soft">
      {reduced ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={poster} alt={title} width={960} height={540} className="h-full w-full object-cover" />
      ) : (
        <>
          <video ref={ref} className="h-full w-full object-cover" autoPlay muted loop playsInline preload="metadata" poster={poster} aria-label={title}>
            <source src={src} type="video/mp4" />
          </video>
          <button type="button" onClick={toggle} aria-label={paused ? 'Play background video' : 'Pause background video'} className="absolute bottom-3 right-3 grid h-10 w-10 place-items-center rounded-full bg-white/90 text-ink shadow-soft transition hover:bg-brand-400">
            {paused ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z" /></svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z" /></svg>
            )}
          </button>
        </>
      )}
    </div>
  );
}
