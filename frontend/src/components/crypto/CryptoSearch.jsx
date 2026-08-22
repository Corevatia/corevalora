import { useState } from "react";
import {
  useCryptoprice,
  useCryptoSearch,
  useSaveTransaction,
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
  const { save, error: saveError } = useSaveTransaction();

  async function handleConfirm({ side, amount, price, tradedOn }) {
    if (!data?.symbol) return;
    try {
      await save({
        asset: data.name,
        key: data.key,
        symbol: data.symbol,
        kind: "crypto",
        side,
        amount,
        price,
        traded_on: tradedOn,
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
    <div className="flex flex-col gap-3 p-2">
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

      {saveError && (
        <p>
          {saveError.status === 409
            ? "You do not hold enough of this asset"
            : `Could not save holding: ${saveError.message}`}
        </p>
      )}
    </div>
  );
}
