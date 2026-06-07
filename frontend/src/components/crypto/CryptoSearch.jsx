import { useState } from "react";
import {
  useCryptoprice,
  useCryptoSearch,
  useSaveHolding,
} from "../../features/hooks.js";
import { SearchBar } from "../shared/SearchBar.jsx";
import AddHoldingForm from "../shared/AddHoldingForm.jsx";
import CryptoSearchResults from "./CryptoSearchResults.jsx";

export default function CryptoSearch({ onSaved }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [selectedKey, setSelectedKey] = useState(null);

  const {
    data: searchdata,
    loading: searchloading,
    error: searchError,
  } = useCryptoSearch(query);
  const { data, loading, error } = useCryptoprice(selectedKey);
  const { save, error: saveError } = useSaveHolding();

  async function handleConfirm({ amount, buyPrice }) {
    if (!data?.symbol) return;
    try {
      await save({
        asset: data.name,
        key: data.key,
        symbol: data.symbol,
        kind: "crypto",
        amount,
        buy_price: buyPrice,
      });
      setSelectedKey(null);
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

      {selectedKey ? (
        <AddHoldingForm
          data={data}
          loading={loading}
          error={error}
          onConfirm={handleConfirm}
        />
      ) : (
        <CryptoSearchResults
          searchdata={searchdata}
          loading={searchloading}
          error={searchError}
          onSelect={setSelectedKey}
        />
      )}

      {saveError && <p>Could not save holding: {saveError.message}</p>}
    </div>
  );
}
