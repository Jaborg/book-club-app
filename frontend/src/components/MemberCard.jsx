import { Link } from "react-router-dom";

export default function MemberCard({ member }) {
  return (
    <div className="card">
      <h3>{member.name}</h3>
      <Link to={`/members/${member.id}`}>View details</Link>
    </div>
  );
}
