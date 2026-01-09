import { useEffect, useState } from "react";
import { getBooks } from "../api/books";
import BookCard from "../components/BookCard";

export default function Books() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    getBooks().then(setBooks);
  }, []);

  return (
    <>
      <h1>Current Books</h1>
      {books.map(book => (
        <BookCard key={book.id} book={book} />
      ))}
    </>
  );
}
