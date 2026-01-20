import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getGroups, createGroup } from "../api/groups";
import { getMembers } from "../api/members";
import { getBooks } from "../api/books";

export default function Groups() {
    const [groups, setGroups] = useState([]);
    const [members, setMembers] = useState([]);
    const [books, setBooks] = useState([]);

    const [name, setName] = useState("");
    const [selectedMemberIds, setSelectedMemberIds] = useState([]);
    const [activeBookId, setActiveBookId] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchAll();
        getMembers().then(setMembers);
        getBooks().then(setBooks);
    }, []);

    const fetchAll = () => getGroups().then(setGroups);

    const toggleMember = (id) => {
        setSelectedMemberIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
    };

    const submit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await createGroup({ name, member_ids: selectedMemberIds, active_book_id: activeBookId || null });
            setName("");
            setSelectedMemberIds([]);
            setActiveBookId("");
            fetchAll();
        } catch (err) {
            console.error(err);
            alert("Failed to create group");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Book Groups</h1>

            <section style={{ display: "grid", gap: 12, gridTemplateColumns: "1fr 360px" }}>
                <div>
                    <h2>Groups</h2>
                    <ul>
                        {groups.map((g) => (
                            <li key={g.id} style={{ marginBottom: 8 }}>
                                <Link to={`/groups/${g.id}`}>{g.name}</Link>
                                {g.active_book && <span style={{ marginLeft: 8, color: "var(--muted)" }}>| Active: {g.active_book.name}</span>}
                            </li>
                        ))}
                    </ul>
                </div>

                <aside>
                    <h2>Create group</h2>
                    <form onSubmit={submit}>
                        <label>
                            Name
                            <input value={name} onChange={(e) => setName(e.target.value)} required style={{ display: "block", width: "100%", padding: 8 }} />
                        </label>

                        <div style={{ marginTop: 8 }}>
                            <div style={{ fontWeight: 700 }}>Members</div>
                            <div style={{ maxHeight: 120, overflow: "auto", border: "1px solid rgba(255,255,255,0.04)", padding: 6 }}>
                                {members.map((m) => (
                                    <label key={m.id} style={{ display: "block" }}>
                                        <input type="checkbox" checked={selectedMemberIds.includes(m.id)} onChange={() => toggleMember(m.id)} /> {m.name}
                                    </label>
                                ))}
                            </div>
                        </div>

                        <label style={{ display: "block", marginTop: 8 }}>
                            Active Book
                            <select value={activeBookId} onChange={(e) => setActiveBookId(e.target.value)} style={{ display: "block", width: "100%", padding: 8 }}>
                                <option value="">(none)</option>
                                {books.map((b) => (
                                    <option key={b.id} value={b.id}>{b.name}</option>
                                ))}
                            </select>
                        </label>

                        <div style={{ marginTop: 8 }}>
                            <button className="btn btn-primary" disabled={loading} type="submit">{loading ? "Creating..." : "Create group"}</button>
                        </div>
                    </form>
                </aside>
            </section>
        </div>
    );
}
