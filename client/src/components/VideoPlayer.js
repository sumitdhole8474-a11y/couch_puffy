'use client';

import { useState } from 'react';

// Click-to-play: the video file is only requested after the visitor presses play (saves bandwidth).
export default function VideoPlayer({ video }) {
  const [playing, setPlaying] = useState(false);

  return (
    <div className="relative aspect-video overflow-hidden rounded-2xl bg-ink shadow-soft">
      {playing ? (
        <video src={video.src} poster={video.poster} controls autoPlay playsInline preload="auto" className="h-full w-full" aria-label={video.title} />
      ) : (
        <button type="button" onClick={() => setPlaying(true)} aria-label={`Play video: ${video.title}`} className="group absolute inset-0 h-full w-full">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={video.poster} alt="" width={1280} height={720} loading="lazy" decoding="async" className="h-full w-full object-cover" />
          <span className="absolute inset-0 grid place-items-center bg-ink/10 transition group-hover:bg-ink/25">
            <span className="grid h-16 w-16 place-items-center rounded-full bg-brand-400 text-ink shadow-soft transition group-hover:scale-110">
              <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z" /></svg>
            </span>
          </span>
          <span className="absolute bottom-3 right-3 rounded-full bg-ink/80 px-2.5 py-0.5 text-xs font-medium text-white">{video.duration}</span>
        </button>
      )}
    </div>
  );
}
