import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <nav className="nav">
      <Link to="/">Book Club</Link>
      <Link to="/books">Books</Link>
      <Link to="/members">Members</Link>
    </nav>
  );
}