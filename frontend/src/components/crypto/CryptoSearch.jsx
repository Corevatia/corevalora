import { useCryptoprice } from "../../features/hooks.js";
import { PriceCard } from "../shared/PriceCard.jsx";
import { SearchBar } from "../shared/SearchBar.jsx";
import { useState } from "react";

export default function CryptoSearch({ onAddHolding }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [amount, setAmount] = useState("");

  const { data, loading, error } = useCryptoprice(query);

  function saveHolding() {
    if (!data?.symbol) return;
    const amt = Number(amount);
    if (!Number.isFinite(amt) || amt <= 0) return;

    onAddHolding({
      asset: data.name,
      symbol: data.symbol,
      amount: amt,
      price: Number(data.price),
      date: data.date,
      currency: data.currency,
    });

    setAmount("");
    setShowAdd(false);
  }
  function onKeyDown(e) {
    if (e.key === "Enter") {
      setQuery(inputValue.trim().toLowerCase());
    }
  }
  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>CryptoSearch</h1>

      <SearchBar
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={onKeyDown}
      />
      {!loading && !error && data?.name && (
        <PriceCard asset={data.name} price={data.price} />
      )}
      {loading && !error && <p>Loading...</p>}
      {data?.name && !showAdd && (
        <button onClick={() => setShowAdd(true)}>Add Holding</button>
      )}
      {error && <p>An Error has occured</p>}

      {data?.name && showAdd && !error && (
        <div>
          <input
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Amount (e.g. 0.5)"
          />
          <button onClick={saveHolding}>Confirm</button>
        </div>
      )}
    </div>
  );
}
