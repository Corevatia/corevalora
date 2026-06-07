import { useState, useMemo } from "react";
import {
  useSaveHolding,
  useStockSearch,
  useStockSearchBackup,
  useStockprice,
} from "../../features/hooks";
import { SearchBar } from "../shared/SearchBar";
import StockSearchResults from "./StockSearchResults";
import AddHoldingForm from "../shared/AddHoldingForm";

export default function StockSearch({ onSaved }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [selectedKey, setSelectedKey] = useState(null);
  const [extendedSearch, setExtendedSearch] = useState(false);

  const {
    data: searchdata,
    loading: searchloading,
    error: searchError,
  } = useStockSearch(query);
  const {
    data: rawExtendedsearchdata,
    loading: extendedSearchLoading,
    error: extendedSearchError,
  } = useStockSearchBackup(query, extendedSearch);
  const existingSymbols = useMemo(
    () => new Set((searchdata ?? []).map((r) => r.symbol)),
    [searchdata],
  );
  const extendedsearchdata = useMemo(
    () =>
      (rawExtendedsearchdata ?? []).filter(
        (r) => !existingSymbols.has(r.symbol),
      ),
    [rawExtendedsearchdata, existingSymbols],
  );
  const {
    data: stockdata,
    loading: stockDataLoading,
    error: stockDataError,
  } = useStockprice(selectedKey);

  const { save, error: saveError } = useSaveHolding();

  async function handleConfirm({ amount, buyPrice }) {
    if (!stockdata?.symbol) return;

    try {
      await save({
        asset: stockdata.name,
        key: stockdata.key,
        symbol: stockdata.symbol,
        kind: "stock",
        amount,
        buy_price: buyPrice,
      });
      setSelectedKey(null);
      onSaved?.();
    } catch {
      //
    }
  }

  function onKeyDown(e) {
    if (e.key === "Enter") {
      setExtendedSearch(false);
      setQuery(inputValue.trim().toLowerCase());
    }
  }

  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>StockSearch</h1>

      <SearchBar
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={onKeyDown}
      />

      {selectedKey ? (
        <AddHoldingForm
          data={stockdata}
          loading={stockDataLoading}
          error={stockDataError}
          onConfirm={handleConfirm}
        />
      ) : (
        <StockSearchResults
          searchdata={searchdata}
          loading={searchloading}
          error={searchError}
          extendedloading={extendedSearchLoading}
          extendederror={extendedSearchError}
          extendedsearchdata={extendedsearchdata}
          extendedSearch={extendedSearch}
          onExtend={() => setExtendedSearch(true)}
          onSelect={setSelectedKey}
        />
      )}

      {saveError && <p>Could not save holding: {saveError.message}</p>}
    </div>
  );
}
