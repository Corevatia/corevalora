import { useState } from "react";
import {
  useAssetPrice,
  useHoldings,
  useSaveTransaction,
} from "../features/hooks";
import { useLocalStorage } from "../hooks/useLocalStorage";
import { SearchBar } from "../components/shared/SearchBar";
import AddHoldingForm from "../components/shared/AddHoldingForm";
import SearchTabs from "../components/search/SearchTabs";
import StockResults from "../components/search/StockResults";
import CryptoResults from "../components/search/CryptoResults";
import MetalResults from "../components/search/MetalResults";
import MetalVariantMenu from "../components/search/MetalVariantMenu";
import NewMetalHolding from "../components/search/NewMetalHolding";

const RESULTS = {
  stock: StockResults,
  crypto: CryptoResults,
  metal: MetalResults,
};

export default function Search({ onClose }) {
  const [kind, setKind] = useLocalStorage("search-kind", "stock");
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [step, setStep] = useState("results");
  const [selectedKey, setSelectedKey] = useState(null);
  const [draft, setDraft] = useState(null);

  const { data, loading, error } = useAssetPrice(kind, selectedKey);
  const { save, error: saveError } = useSaveTransaction();
  const {
    holdings,
    loading: holdingsLoading,
    error: holdingsError,
  } = useHoldings();

  const Results = RESULTS[kind];
  const variants = (holdings ?? []).filter(
    (holding) => holding.kind === "metal" && holding.key === selectedKey,
  );

  function resetToResults() {
    setStep("results");
    setSelectedKey(null);
    setDraft(null);
  }

  function handleKindChange(nextKind) {
    setKind(nextKind);
    resetToResults();
  }

  function onKeyDown(e) {
    if (e.key === "Enter") {
      setQuery(inputValue.trim().toLowerCase());
      resetToResults();
    }
  }

  function handleSelect(key) {
    setSelectedKey(key);
    setStep(kind === "metal" ? "variants" : "form");
  }

  function handlePickVariant(holding) {
    setDraft({ customName: holding.customName, unit: holding.unit });
    setStep("form");
  }

  function handleNewVariant(newDraft) {
    setDraft(newDraft);
    setStep("form");
  }

  function handleBack() {
    if (step === "new") {
      setStep("variants");
      return;
    }
    if (step === "form" && kind === "metal") {
      setDraft(null);
      setStep("variants");
      return;
    }
    resetToResults();
  }

  async function handleConfirm({ side, amount, price, tradedOn }) {
    if (!data?.symbol) return;
    try {
      await save({
        asset: data.name,
        key: data.key,
        symbol: data.symbol,
        kind,
        unit: draft?.unit,
        custom_name: draft?.customName,
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
            onClick={handleBack}
            className="pb-2 font-semibold hover:underline"
          >
            ← Back
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

        {step === "results" && (
          <Results query={query} onSelect={handleSelect} />
        )}
        {step === "variants" && (
          <MetalVariantMenu
            variants={variants}
            loading={holdingsLoading}
            error={holdingsError}
            onPick={handlePickVariant}
            onCreate={() => setStep("new")}
          />
        )}

        {step === "new" && (
          <NewMetalHolding variants={variants} onSubmit={handleNewVariant} />
        )}

        {step === "form" && (
          <AddHoldingForm
            data={data}
            unit={draft?.unit}
            customName={draft?.customName}
            loading={loading}
            error={error}
            onConfirm={handleConfirm}
          />
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
