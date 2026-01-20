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
      <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
        <img
          src={`https://api.dicebear.com/9.x/identicon/svg?seed=${encodeURIComponent(
            String(member.name ?? member.email ?? member.id)
          )}&size=256`}
          alt={`${member.name} avatar`}
          style={{ width: 96, height: 128, borderRadius: 12 }}
        />

        <div>
          <h1>{member.name}</h1>
          <div className="muted">Id: {member.id}</div>
        </div>
      </div>

      <h3 style={{ marginTop: 18 }}>{member.name} has assigned</h3>
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
