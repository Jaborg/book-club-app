const BASE = "/api";

export const getBooks = async () => {
  const res = await fetch(`${BASE}/books/`);
  return res.json();
};

export const getBook = async (id) => {
  const res = await fetch(`${BASE}/books/${id}`);
  return res.json();
};
