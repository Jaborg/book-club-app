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

  // Fetch books on load
  useEffect(() => {
    fetch(`${API_URL}/books/`)
      .then((res) => res.json())
      .then(setBooks)
      .catch(() => setError("Failed to load books"))
      .finally(() => setLoading(false));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    // 1️⃣ Optimistic book
    const optimisticBook = {
      id: `temp-${Date.now()}`,
      ...form
    };

    setBooks((prev) => [optimisticBook, ...prev]);

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

      if (!res.ok) {
        throw new Error("Failed to create book");
      }

      const savedBook = await res.json();

      // 2️⃣ Replace optimistic book with real one
      setBooks((prev) =>
        prev.map((b) => (b.id === optimisticBook.id ? savedBook : b))
      );

      // Reset form
      setForm({
        name: "",
        author: "",
        member_id: "",
        due_date: "",
        rating: ""
      });
    } catch (err) {
      // 3️⃣ Rollback optimistic update
      setBooks((prev) =>
        prev.filter((b) => b.id !== optimisticBook.id)
      );
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
