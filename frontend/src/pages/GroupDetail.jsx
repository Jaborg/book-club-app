import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getGroup, addMember, removeMember, setActiveBook } from "../api/groups";
import { getMembers } from "../api/members";
import { getBooks } from "../api/books";

export default function GroupDetail() {
    const { id } = useParams();
    const [group, setGroup] = useState(null);
    const [allMembers, setAllMembers] = useState([]);
    const [allBooks, setAllBooks] = useState([]);
    const [selectedAddMember, setSelectedAddMember] = useState("");
    const [selectedBook, setSelectedBook] = useState("");

    const fetch = () => getGroup(id).then(setGroup);

    useEffect(() => {
        fetch();
        getMembers().then(setAllMembers);
        getBooks().then(setAllBooks);
    }, [id]);

    const handleAdd = async () => {
        if (!selectedAddMember) return;
        await addMember(id, Number(selectedAddMember));
        setSelectedAddMember("");
        fetch();
    };

    const handleRemove = async (memberId) => {
        await removeMember(id, memberId);
        fetch();
    };

    const handleSetActive = async () => {
        if (!selectedBook) return;
        await setActiveBook(id, Number(selectedBook));
        fetch();
    };

    if (!group) return <p>Loading...</p>;

    const memberIds = new Set(group.members.map((m) => m.id));

    return (
        <div>
            <h1>{group.name}</h1>

            <div style={{ display: "flex", gap: 24 }}>
                <section style={{ minWidth: 320 }}>
                    <h3>Members</h3>
                    <ul>
                        {group.members.map((m) => (
                            <li key={m.id} style={{ marginBottom: 8 }}>
                                {m.name} <button className="btn btn-ghost" style={{ marginLeft: 8 }} onClick={() => handleRemove(m.id)}>Remove</button>
                            </li>
                        ))}
                    </ul>

                    <div style={{ marginTop: 12 }}>
                        <select value={selectedAddMember} onChange={(e) => setSelectedAddMember(e.target.value)}>
                            <option value="">Select member to add</option>
                            {allMembers.filter((m) => !memberIds.has(m.id)).map((m) => (
                                <option key={m.id} value={m.id}>{m.name}</option>
                            ))}
                        </select>
                        <button className="btn btn-primary" onClick={handleAdd} style={{ marginLeft: 8 }}>Add</button>
                    </div>
                </section>

                <section>
                    <h3>Active book</h3>
                    <div>
                        {group.active_book ? (
                            <div>{group.active_book.name} — {group.active_book.author}</div>
                        ) : (
                            <div><em>None</em></div>
                        )}
                    </div>

                    <div style={{ marginTop: 8 }}>
                        <select value={selectedBook} onChange={(e) => setSelectedBook(e.target.value)}>
                            <option value="">Select book</option>
                            {allBooks.map((b) => (
                                <option key={b.id} value={b.id}>{b.name}</option>
                            ))}
                        </select>
                        <button className="btn btn-primary" style={{ marginLeft: 8 }} onClick={handleSetActive}>Set active</button>
                    </div>
                </section>
            </div>
        </div>
    );
}
