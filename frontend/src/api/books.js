const BASE = "/api";

export const getBooks = async () => {
  const res = await fetch(`${BASE}/books/`);
  return res.json();
};

export const getBook = async (id) => {
  const res = await fetch(`${BASE}/books/${id}`);
  return res.json();
};

// Client-side cache for book cover lookups stored in localStorage under this key.
const COVER_CACHE_KEY = "book_cover_cache_v1";
// Cache TTL in milliseconds (30 days)
const CACHE_TTL_MS = 1000 * 60 * 60 * 24 * 30;

const loadCache = () => {
  try {
    const raw = localStorage.getItem(COVER_CACHE_KEY);
    if (!raw) return {};
    return JSON.parse(raw);
  } catch (e) {
    return {};
  }
};

const saveCache = (cache) => {
  try {
    localStorage.setItem(COVER_CACHE_KEY, JSON.stringify(cache));
  } catch (e) {
    // ignore quota errors
  }
};

const makeKey = (title, author) => {
  const t = (title || "").trim().toLowerCase();
  const a = (author || "").trim().toLowerCase();
  return `${t}::${a}`;
};

// Try to get a cover image URL for a book using the Google Books API.
// Uses localStorage cache to avoid repeated lookups. Returns a thumbnail URL string or null if not found.
export const getBookCover = async (title, author) => {
  const key = makeKey(title, author);
  const cache = loadCache();

  const entry = cache[key];
  const now = Date.now();
  if (entry && typeof entry.url !== "undefined") {
    // check TTL
    if (!entry.ts || now - entry.ts < CACHE_TTL_MS) {
      return entry.url;
    }
    // expired: fall through to refetch
  }

  try {
    const q = [];
    if (title) q.push(`intitle:${encodeURIComponent(title)}`);
    if (author) q.push(`inauthor:${encodeURIComponent(author)}`);
    const query = q.length ? q.join("+") : encodeURIComponent(title || author || "");
    const url = `https://www.googleapis.com/books/v1/volumes?q=${query}&maxResults=5`;
    const res = await fetch(url);
    if (!res.ok) {
      // cache negative result to avoid repeats
      cache[key] = { url: null, ts: now };
      saveCache(cache);
      return null;
    }
    const data = await res.json();
    if (!data.items || data.items.length === 0) {
      cache[key] = { url: null, ts: now };
      saveCache(cache);
      return null;
    }

    // Prefer the first item with an image link
    for (const item of data.items) {
      const links = item.volumeInfo?.imageLinks;
      if (links?.thumbnail) {
        const cleaned = links.thumbnail.replace("http://", "https://");
        cache[key] = { url: cleaned, ts: now };
        saveCache(cache);
        return cleaned;
      }
      if (links?.smallThumbnail) {
        const cleaned = links.smallThumbnail.replace("http://", "https://");
        cache[key] = { url: cleaned, ts: now };
        saveCache(cache);
        return cleaned;
      }
    }

    cache[key] = { url: null, ts: now };
    saveCache(cache);
    return null;
  } catch (e) {
    // on error, cache negative result and return null
    cache[key] = { url: null, ts: now };
    saveCache(cache);
    return null;
  }
};
