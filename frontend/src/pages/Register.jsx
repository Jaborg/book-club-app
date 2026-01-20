import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register, login } from "../api/auth";

export default function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const submit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            await register(name, email, password);
            // auto-login after register
            const data = await login(email, password);
            localStorage.setItem("access_token", data.access_token);
            navigate("/");
        } catch (err) {
            setError(err.message || "Registration failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Create an account</h2>
            <form onSubmit={submit} style={{ maxWidth: 480 }}>
                <label style={{ display: "block", marginTop: 8 }}>
                    Name
                    <input required type="text" value={name} onChange={(e) => setName(e.target.value)} style={{ display: "block", width: "100%", padding: "8px", marginTop: 6 }} />
                </label>

                <label style={{ display: "block", marginTop: 8 }}>
                    Email
                    <input required type="email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ display: "block", width: "100%", padding: "8px", marginTop: 6 }} />
                </label>

                <label style={{ display: "block", marginTop: 8 }}>
                    Password
                    <input required type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ display: "block", width: "100%", padding: "8px", marginTop: 6 }} />
                </label>

                <div style={{ marginTop: 12 }}>
                    <button className="btn btn-primary" disabled={loading} type="submit">{loading ? "Creating..." : "Create account"}</button>
                </div>

                {error && <p style={{ color: "#ffb4b4", marginTop: 12 }}>{error}</p>}
            </form>
        </div>
    );
}
