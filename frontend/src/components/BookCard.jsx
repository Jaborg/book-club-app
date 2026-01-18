import { Link } from "react-router-dom";

export default function BookCard({ book }) {
  return (
    <article className="card">
      <div className="card-row">
        <div className="cover" aria-hidden />

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
