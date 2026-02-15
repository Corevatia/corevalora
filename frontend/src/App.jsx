import { useEffect, useState } from "react";

export default function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/crypto/price/bitcoin")
      .then((r) => r.json())
      .then(setData);
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>CoreValora</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
