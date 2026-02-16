import { useCryptoprice } from "../features/crypto/hooks";
import { PriceCard } from "../components/crypto/PriceCard";
import { SearchBar } from "../components/crypto/SearchBar";
import { useState } from "react";

export default function CryptoSearchPage() {
  const [query, setQuery] = useState("");

  const data = useCryptoprice(query);

  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>CryptoSearch</h1>

      <SearchBar
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <PriceCard asset={query} price={data?.priceUsd} />
    </div>
  );
}