import { useEffect, useState } from "react";
import { getMembers } from "../api/members";
import MemberCard from "../components/MemberCard";

export default function Members() {
  const [members, setMembers] = useState([]);

  useEffect(() => {
    getMembers().then(setMembers);
  }, []);

  return (
    <>
      <h1>Members</h1>
      {members.map(m => (
        <MemberCard key={m.id} member={m} />
      ))}
    </>
  );
}
