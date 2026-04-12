import { useState } from "react";
import {
  useStockSearch,
  useStockSearchBackup,
  useStockprice,
} from "../../features/hooks";
import { SearchBar } from "../shared/SearchBar";
import StockData from "./StockData";
import StockSearchResults from "./StockSearchResults";
import AddHoldingForm from "./AddHoldingForm";

export default function StockSearch({ onAddHolding }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [amount, setAmount] = useState("");
  const [stockSymbol, setStockSymbol] = useState("");
  const [showSearch, setShowSearch] = useState(true);
  const [extendedSearch, setExtendedSearch] = useState(false);

  const searchdata = useStockSearch(query);
  const rawExtendedsearchdata = useStockSearchBackup(query, extendedSearch);
  const existingSymbols = new Set((searchdata ?? []).map((r) => r.symbol));
  const extendedsearchdata = (rawExtendedsearchdata ?? []).filter(
    (r) => !existingSymbols.has(r.symbol),
  );
  const stockdata = useStockprice(stockSymbol);

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
    setShowAdd(false);
    setShowSearch(true);
  }
  function onKeyDown(e) {
    if (e.key === "Enter") {
      setExtendedSearch(false);
      setQuery(inputValue.trim());
    }
  }
  function Select(symbol) {
    setShowAdd(true);
    setStockSymbol(symbol);
    setShowSearch(false);
  }
  function Extend() {
    setExtendedSearch(true);
  }
  function Confirm() {
    saveHolding();
  }
  function AmountChange(value) {
    setAmount(value);
    setExtendedSearch(false);
  }
  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>StockSearch</h1>

      <SearchBar
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={onKeyDown}
      />

      {showSearch &&
        StockSearchResults({
          searchdata: searchdata,
          extendedsearchdata: extendedsearchdata,
          extendedSearch: extendedSearch,
          showAdd: showAdd,
          onExtend: Extend,
          onSelect: Select,
        })}
      {!showSearch &&
        AddHoldingForm({
          stockdata: stockdata,
          onConfirm: Confirm,
          amount: amount,
          onAmountChange: AmountChange,
        })}
    </div>
  );
}
