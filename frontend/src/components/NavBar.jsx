import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function NavBar() {
  const [token, setToken] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    setToken(localStorage.getItem("access_token"));
  }, []);

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    navigate("/");
  };

  return (
    <nav className="nav">
      <div className="container nav-inner">
        <Link to="/" className="brand">
          <span className="logo" aria-hidden>
            📚
          </span>
          <span className="brand-text">FatDogReads</span>
        </Link>

        <div className="nav-links" role="navigation" aria-label="Primary">
          <Link to="/books">Books</Link>
          <Link to="/members">Members</Link>
          {!token ? (
            <Link to="/login">Login</Link>
          ) : (
            <button onClick={logout} className="btn btn-ghost" style={{ marginLeft: 12 }}>
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}