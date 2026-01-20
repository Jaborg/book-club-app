import { authFetch } from "./auth";

const BASE = "/api";

export const getGroups = async () => {
    const res = await fetch(`${BASE}/groups/`);
    return res.json();
};

export const getGroup = async (id) => {
    const res = await fetch(`${BASE}/groups/${id}`);
    return res.json();
};

export const createGroup = async (payload) => {
    const res = await authFetch(`${BASE}/groups/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    return res.json();
};

export const addMember = async (groupId, memberId) => {
    const res = await authFetch(`${BASE}/groups/${groupId}/add_member`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ member_id: memberId }),
    });
    return res.json();
};

export const removeMember = async (groupId, memberId) => {
    const res = await authFetch(`${BASE}/groups/${groupId}/remove_member`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ member_id: memberId }),
    });
    return res.json();
};

export const setActiveBook = async (groupId, bookId) => {
    const res = await authFetch(`${BASE}/groups/${groupId}/set_active_book`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ book_id: bookId }),
    });
    return res.json();
};
