import React, { useEffect, useState } from "react";

function App() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  const fetchUsers = async () => {
    const res = await fetch("/users");
    const data = await res.json();
    setUsers(data);
  };

  const addUser = async (e) => {
    e.preventDefault();o
    const res = await fetch("/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    const data = await res.json();
    setMessage(data.message || data.error);
    setName("");
    fetchUsers();
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>👤 User Manager</h1>

      <form onSubmit={addUser}>
        <input
          type="text"
          placeholder="Enter name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <button type="submit">Add User</button>
      </form>

      <p>{message}</p>

      <h2>Existing Users:</h2>
      <ul>
        {users.map((u, i) => (
          <li key={i}>{u}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
