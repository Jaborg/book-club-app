import { Link } from "react-router-dom";

export default function MemberCard({ member }) {
  // Use member name as the deterministic seed for avatars. Fall back to email/id if name missing.
  const seed = member?.name ?? member?.email ?? member?.id ?? String(Math.random());
  // New DiceBear 9.x API endpoint with style 'identicon' and size param for consistent images
  const avatar = `https://api.dicebear.com/9.x/identicon/svg?seed=${encodeURIComponent(
    String(seed)
  )}&size=96`;

  return (
    <article className="card">
      <div className="card-row">
        <img className="cover" src={avatar} alt={`${member.name} avatar`} />
        <div style={{ flex: 1 }}>
          <h3>{member.name}</h3>
          <p className="muted">Member ID: {member.id}</p>
          <div className="actions">
            <Link className="btn btn-primary" to={`/members/${member.id}`}>
              View details
            </Link>
            <button className="btn btn-ghost" type="button">
              Message
            </button>
          </div>
        </div>
      </div>
    </article>
  );
}
