const BASE = "/api";

export const getMembers = async () => {
  const res = await fetch(`${BASE}/members/`);
  return res.json();
};

export const getMember = async (id) => {
  const res = await fetch(`${BASE}/members/${id}`);
  return res.json();
};
