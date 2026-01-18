import { Link } from "react-router-dom";

export default function MemberCard({ member }) {
  return (
    <article className="card">
      <div className="card-row">
        <div className="cover" aria-hidden />
        <div style={{ flex: 1 }}>
          <h3>{member.name}</h3>
          <p className="muted">Member ID: {member.id}</p>
          <div className="actions">
            <Link className="btn btn-primary" to={`/members/${member.id}`}>View details</Link>
            <button className="btn btn-ghost" type="button">Message</button>
          </div>
        </div>
      </div>
    </article>
  );
}
