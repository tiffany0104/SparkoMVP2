import React, { useEffect, useState } from "react";
import SwipeStack from "./SwipeStack";

function App() {
  const [profiles, setProfiles] = useState([]);

  useEffect(() => {
    fetch("/api/profiles")
      .then((res) => res.json())
      .then((data) => setProfiles(data))
      .catch((err) => console.error("Failed to load profiles:", err));
  }, []);

  return (
    <div className="app">
      <SwipeStack profiles={profiles} />
    </div>
  );
}

export default App;
