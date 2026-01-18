import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <nav className="nav">
      <div className="container nav-inner">
        <Link to="/" className="brand">
          <span className="logo" aria-hidden>📚</span>
          <span className="brand-text">Book Club</span>
        </Link>

        <div className="nav-links" role="navigation" aria-label="Primary">
          <Link to="/books">Books</Link>
          <Link to="/members">Members</Link>
        </div>
      </div>
    </nav>
  );
}