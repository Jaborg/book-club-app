import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getBook, getBookCover } from "../api/books";

export default function BookDetail() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [cover, setCover] = useState(null);

  useEffect(() => {
    getBook(id).then(setBook);
  }, [id]);

  useEffect(() => {
    let mounted = true;
    if (!book) return;
    (async () => {
      const url = await getBookCover(book.name, book.author).catch(() => null);
      if (!mounted) return;
      if (url) setCover(url);
      else {
        const seed = book.member?.name ?? book.name ?? String(Math.random());
        setCover(`https://api.dicebear.com/9.x/identicon/svg?seed=${encodeURIComponent(seed)}&size=256`);
      }
    })();

    return () => {
      mounted = false;
    };
  }, [book]);

  if (!book) return <p>Loading...</p>;

  return (
    <>
      <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
        {cover && (
          <img src={cover} alt={`${book.name} cover`} style={{ width: 120, height: 160, borderRadius: 8 }} />
        )}
        <h1>{book.name}</h1>
      </div>

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
