import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getBook } from "../api/books";

export default function BookDetail() {
  const { id } = useParams();
  const [book, setBook] = useState(null);

  useEffect(() => {
    getBook(id).then(setBook);
  }, [id]);

  if (!book) return <p>Loading...</p>;

  return (
    <>
      <h1>{book.name}</h1>

      <p><strong>Author:</strong> {book.author}</p>
      <p><strong>Rating:</strong> {book.rating}</p>
      <p>
        <strong>Due date:</strong>{" "}
        {new Date(book.due_date).toLocaleDateString()}
      </p>

      <p>
        <strong>Assigned member:</strong>{" "}
        {book.member ? (
          <Link to={`/members/${book.member.id}`}>
            {book.member.name}
          </Link>
        ) : (
          "None"
        )}
      </p>
    </>
  );
}
