import { useState } from "react";
import { useAssetPrice, useSaveTransaction } from "../features/hooks";
import { useLocalStorage } from "../hooks/useLocalStorage";
import { SearchBar } from "../components/shared/SearchBar";
import AddHoldingForm from "../components/shared/AddHoldingForm";
import SearchTabs from "../components/search/SearchTabs";
import StockResults from "../components/search/StockResults";
import CryptoResults from "../components/search/CryptoResults";
import MetalResults from "../components/search/MetalResults";

const RESULTS = {
  stock: StockResults,
  crypto: CryptoResults,
  metal: MetalResults,
};

export default function Search({ onClose }) {
  const [kind, setKind] = useLocalStorage("search-kind", "stock");
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [selectedKey, setSelectedKey] = useState(null);

  const { data, loading, error } = useAssetPrice(kind, selectedKey);
  const { save, error: saveError } = useSaveTransaction();

  const Results = RESULTS[kind];

  function handleKindChange(nextKind) {
    setKind(nextKind);
    setSelectedKey(null);
  }

  function onKeyDown(e) {
    if (e.key === "Enter") {
      setQuery(inputValue.trim().toLowerCase());
      setSelectedKey(null);
    }
  }

  async function handleConfirm({ side, amount, price, tradedOn }) {
    if (!data?.symbol) return;
    try {
      await save({
        asset: data.name,
        key: data.key,
        symbol: data.symbol,
        kind,
        side,
        amount,
        price,
        traded_on: tradedOn,
      });
      onClose();
    } catch {
      // saveError is rendered below
    }
  }

  return (
    <div className="flex justify-center">
      <div className="flex w-full max-w-xl flex-col gap-3 p-4">
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={() => setSelectedKey(null)}
            className="pb-2 font-semibold hover:underline"
          >
            ← Back to results
          </button>
          <button
            type="button"
            aria-label="Cancel"
            onClick={onClose}
            className="rounded-xl px-3 py-1 text-2xl hover:bg-mist-100 dark:hover:bg-mist-900"
          >
            ✕
          </button>
        </div>
        <div>
          <h2 className="text-center p-1 text-3xl font-extrabold">
            Add Holding
          </h2>
        </div>
        <SearchBar
          inputValue={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={onKeyDown}
        />

        <SearchTabs kind={kind} onChange={handleKindChange} />

        {selectedKey ? (
          <div>
            <AddHoldingForm
              data={data}
              loading={loading}
              error={error}
              onConfirm={handleConfirm}
            />
          </div>
        ) : (
          <Results query={query} onSelect={setSelectedKey} />
        )}

        {saveError && (
          <p>
            {saveError.status === 409
              ? "You do not hold enough of this asset."
              : `Could not save holding: ${saveError.message}`}
          </p>
        )}
      </div>
    </div>
  );
}
