const BASE = "/api";

export const login = async (email, password) => {
    const res = await fetch(`${BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Login failed");
    }

    return res.json();
};

export const register = async (name, email, password) => {
    const res = await fetch(`${BASE}/members/create_member`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Registration failed");
    }

    return res.json();
};

export const authFetch = async (input, init = {}) => {
    const token = localStorage.getItem("access_token");
    const headers = new Headers(init.headers || {});
    headers.set("Accept", "application/json");
    if (token) headers.set("Authorization", `Bearer ${token}`);

    const res = await fetch(input, { ...init, headers });
    return res;
};

export const decodeJwt = (token) => {
    try {
        const parts = token.split(".");
        if (parts.length !== 3) return null;
        const payload = parts[1].replace(/-/g, "+").replace(/_/g, "/");
        const json = decodeURIComponent(
            atob(payload)
                .split("")
                .map(function (c) {
                    return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
                })
                .join("")
        );
        return JSON.parse(json);
    } catch (e) {
        return null;
    }
};

export const getCurrentMemberIdFromToken = () => {
    const token = localStorage.getItem("access_token");
    if (!token) return null;
    const decoded = decodeJwt(token);
    if (!decoded) return null;
    // sub contains member id per backend token creation
    return decoded.sub ?? decoded.user_id ?? null;
};
