export default function Stars({ rating, reviews }) {
  return (
    <div className="flex items-center gap-1 text-sm text-stone-600">
      <span className="text-brand-500" aria-hidden="true">
        {'★'.repeat(Math.round(rating))}
        <span className="text-stone-300">{'★'.repeat(5 - Math.round(rating))}</span>
      </span>
      <span className="sr-only">{rating} out of 5 stars</span>
      <span>{rating}</span>
      {reviews ? <span className="text-stone-400">({reviews})</span> : null}
    </div>
  );
}
