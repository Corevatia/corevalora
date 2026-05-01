import { useState, useMemo } from "react";
import {
  useStockSearch,
  useStockSearchBackup,
  useStockprice,
} from "../../features/hooks";
import { SearchBar } from "../shared/SearchBar";
import StockSearchResults from "./StockSearchResults";
import AddHoldingForm from "../shared/AddHoldingForm";

export default function StockSearch({ onAddHolding }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [selectedSymbol, setSelectedSymbol] = useState(null);
  const [amount, setAmount] = useState("");
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
  } = useStockprice(selectedSymbol);

  function saveHolding() {
    if (!stockdata?.symbol) return;
    const amt = Number(amount);
    if (!Number.isFinite(amt) || amt <= 0) return;
    onAddHolding({
      asset: stockdata.name,
      symbol: stockdata.symbol,
      amount: amt,
      date: stockdata.date,
      price: Number(stockdata.price),
      exchange: stockdata.exchange,
      currency: stockdata.currency,
    });

    setAmount("");
    setSelectedSymbol(null);
  }

  function onKeyDown(e) {
    if (e.key === "Enter") {
      setExtendedSearch(false);
      setQuery(inputValue.trim());
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

      {selectedSymbol ? (
        <AddHoldingForm
          data={stockdata}
          loading={stockDataLoading}
          error={stockDataError}
          amount={amount}
          onAmountChange={setAmount}
          onConfirm={saveHolding}
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
          onSelect={setSelectedSymbol}
        />
      )}
    </div>
  );
}
