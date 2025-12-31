import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";

function App() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Form state
  const [form, setForm] = useState({
    name: "",
    author: "",
    member_id: "",
    due_date: "",
    rating: ""
  });

  // 🔁 Source-of-truth fetch
  const fetchBooks = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_URL}/books/`);
      if (!res.ok) {
        throw new Error("Failed to load books");
      }
      const data = await res.json();
      setBooks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Load books on mount
  useEffect(() => {
    fetchBooks();
  }, []);

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      const res = await fetch(`${API_URL}/books/create_book`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          ...form,
          member_id: Number(form.member_id),
          due_date: new Date(form.due_date).toISOString(),
          initial_date: new Date().toISOString()
        })
      });

      const payload = await res.json();

      if (!res.ok) {
        throw new Error(payload?.message || "Failed to create book");
      }

      // 🔁 Re-fetch list (single source of truth)
      await fetchBooks();

      // Reset form
      setForm({
        name: "",
        author: "",
        member_id: "",
        due_date: "",
        rating: ""
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page">
      <h1>📚 Book Club</h1>

      {/* FORM */}
      <form className="book-form" onSubmit={handleSubmit}>
        <h2>Add a Book</h2>

        <input
          name="name"
          placeholder="Book title"
          value={form.name}
          onChange={handleChange}
          required
        />

        <input
          name="author"
          placeholder="Author"
          value={form.author}
          onChange={handleChange}
          required
        />

        <input
          name="member_id"
          placeholder="Member ID"
          value={form.member_id}
          onChange={handleChange}
          required
        />

        <input
          type="date"
          name="due_date"
          value={form.due_date}
          onChange={handleChange}
          required
        />

        <input
          name="rating"
          placeholder="Rating (1–5)"
          value={form.rating}
          onChange={handleChange}
          required
        />

        <button disabled={submitting}>
          {submitting ? "Saving..." : "Add Book"}
        </button>
      </form>

      {/* ERROR */}
      {error && <p className="error">{error}</p>}

      {/* LOADING */}
      {loading && <p>Loading books...</p>}

      {/* BOOK LIST */}
      <div className="book-grid">
        {books.map((book) => (
          <div className="book-card" key={book.id}>
            <h3>{book.name}</h3>
            <p>{book.author}</p>
            <p>Member ID: {book.member_id}</p>
            <p>⭐ {book.rating}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
