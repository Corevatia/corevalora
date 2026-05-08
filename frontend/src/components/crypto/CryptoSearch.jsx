import { useState } from "react";
import { useCryptoprice, useSaveHolding } from "../../features/hooks.js";
import { SearchBar } from "../shared/SearchBar.jsx";
import AddHoldingForm from "../shared/AddHoldingForm.jsx";

export default function CryptoSearch({ onSaved }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");

  const { data, loading, error } = useCryptoprice(query);
  const { save, error: saveError } = useSaveHolding();

  async function handleConfirm({ amount, buyPrice }) {
    if (!data?.symbol) return;
    try {
      await save({
        asset: data.name,
        symbol: data.symbol,
        kind: "crypto",
        amount,
        buy_price: buyPrice,
      });
      setInputValue("");
      setQuery("");
      onSaved?.();
    } catch {
      //
    }
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
          onConfirm={handleConfirm}
        />
      )}

      {saveError && <p>Could not save holding: {saveError.message}</p>}
    </div>
  );
}
