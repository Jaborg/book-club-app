import { Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

export default function NavBar() {
  const [token, setToken] = useState(null);
  const navigate = useNavigate();

  const location = useLocation();

  // Update token on mount and when the route changes (e.g. after login navigates)
  useEffect(() => {
    setToken(localStorage.getItem("access_token"));
  }, [location]);

  // Also listen for storage events (cross-tab changes)
  useEffect(() => {
    const onStorage = (e) => {
      if (e.key === "access_token") setToken(e.newValue);
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
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
          <Link to="/groups">Groups</Link>
          {!token ? (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register" style={{ marginLeft: 12 }}>Register</Link>
            </>
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