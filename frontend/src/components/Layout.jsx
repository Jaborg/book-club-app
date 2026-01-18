import { Outlet } from "react-router-dom";
import NavBar from "./NavBar";

export default function Layout() {
  return (
    <>
      <NavBar />

      <div className="hero">
        <div className="container">
          <h1>Book Club</h1>
          <p>Read together. Discuss freely. Discover more books and members.</p>
        </div>
      </div>

      <main className="container">
        <Outlet />
      </main>
    </>
  );
}