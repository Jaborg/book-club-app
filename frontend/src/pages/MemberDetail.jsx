import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getMember } from "../api/members";
import { getBooks } from "../api/books";

export default function MemberDetail() {
  const { id } = useParams();
  const [member, setMember] = useState(null);
  const [books, setBooks] = useState([]);

  useEffect(() => {
    getMember(id).then(setMember);
    getBooks().then(allBooks =>
      setBooks(allBooks.filter(b => b.member?.id === Number(id)))
    );
  }, [id]);

  if (!member) return <p>Loading...</p>;

  return (
    <>
      <h1>{member.name}</h1>

      <h3>Books assigned</h3>
      {books.length === 0 ? (
        <p>No books assigned</p>
      ) : (
        <ul>
          {books.map(b => (
            <li key={b.id}>
              <Link to={`/books/${b.id}`}>{b.name}</Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
