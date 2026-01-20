import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getBookCover } from "../api/books";

export default function BookCard({ book }) {
  const [cover, setCover] = useState(null);

  useEffect(() => {
    let mounted = true;

    (async () => {
      // Try to fetch a cover image from Google Books. If none, use a DiceBear identicon seeded by book name.
      const url = await getBookCover(book.name, book.author).catch(() => null);
      if (!mounted) return;
      if (url) setCover(url);
      else {
        // If the book is assigned to a member, use the member's name as the avatar seed
        const seed = book.member?.name ?? book.name ?? String(Math.random());
        setCover(`https://api.dicebear.com/9.x/identicon/svg?seed=${encodeURIComponent(seed)}&size=96`);
      }
    })();

    return () => {
      mounted = false;
    };
  }, [book.name, book.author]);

  return (
    <article className="card">
      <div className="card-row">
        <img className="cover" src={cover} alt={`${book.name} cover`} />

        <div style={{ flex: 1 }}>
          <h3>{book.name}</h3>

          <div className="meta">
            <span className="badge">Author: {book.author}</span>
            <span className="badge">Rating: {book.rating ?? "—"}</span>
            <span className="badge">Due: {book.due_date ? new Date(book.due_date).toLocaleDateString() : "—"}</span>
          </div>

          {book.member ? (
            <p className="mb-2">
              <strong className="muted">Member:</strong>{" "}
              <Link to={`/members/${book.member.id}`}>{book.member.name}</Link>
            </p>
          ) : (
            <p className="mb-2 muted"><em>No member assigned</em></p>
          )}

          <div className="actions">
            <Link className="btn btn-primary" to={`/books/${book.id}`}>View details</Link>
            <button className="btn btn-ghost" type="button">Reserve</button>
          </div>
        </div>
      </div>
    </article>
  );
}
