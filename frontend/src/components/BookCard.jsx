import { Link } from "react-router-dom";

export default function BookCard({ book }) {
  return (
    <div className="card">
      <h3>{book.name}</h3>
      <p><strong>Author:</strong> {book.author}</p>
      <p><strong>Rating:</strong> {book.rating}</p>
      <p>
        <strong>Due:</strong>{" "}
        {new Date(book.due_date).toLocaleDateString()}
      </p>

      {book.member ? (
        <p>
          <strong>Member:</strong>{" "}
          <Link to={`/members/${book.member.id}`}>
            {book.member.name}
          </Link>
        </p>
      ) : (
        <p><em>No member assigned</em></p>
      )}

      <Link to={`/books/${book.id}`}>View details</Link>
    </div>
  );
}
