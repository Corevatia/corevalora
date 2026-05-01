import { useState } from "react";
import { useCryptoprice } from "../../features/hooks.js";
import { SearchBar } from "../shared/SearchBar.jsx";
import AddHoldingForm from "../shared/AddHoldingForm.jsx";

export default function CryptoSearch({ onAddHolding }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");

  const { data, loading, error } = useCryptoprice(query);

  function saveHolding({ amount, buyPrice }) {
    if (!data?.symbol) return;

    onAddHolding({
      asset: data.name,
      symbol: data.symbol,
      amount,
      buyPrice,
      price: Number(data.price),
      date: data.date,
      currency: data.currency,
    });

    setInputValue("");
    setQuery("");
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

      {query && (
        <AddHoldingForm
          data={data}
          loading={loading}
          error={error}
          onConfirm={saveHolding}
        />
      )}
    </div>
  );
}
