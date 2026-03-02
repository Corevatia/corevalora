import { useState } from "react";
import {
  useStockSearch,
  useStockSearchBackup,
  useStockprice,
} from "../../features/hooks";
import { SearchBar } from "../shared/SearchBar";
import SearchResult from "./SearchResult";
import StockData from "./StockData";

export default function StockSearch({ onAddHolding }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [amount, setAmount] = useState("");
  const [stockSymbol, setStockSymbol] = useState("");
  const [showSearch, setShowSearch] = useState(true);
  const [extendedSearch, setExtendedSearch] = useState(false);

  const searchdata = useStockSearch(query);
  const extendsearchdata = useStockSearchBackup(query, extendedSearch);
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

      <h2>SearchResults:</h2>
      {showSearch &&
        searchdata?.map((r) => (
          <div key={r.symbol}>
            <SearchResult
              name={r.name}
              symbol={r.symbol}
              exchange={r.exchange}
              mic={r.mic}
            />
            {!showAdd && (
              <button
                onClick={() => {
                  setShowAdd(true);
                  setStockSymbol(r.symbol);
                  setShowSearch(false);
                }}
              >
                Add Holding
              </button>
            )}
          </div>
        ))}
      {showSearch &&
        extendsearchdata?.map((r) => (
          <div key={r.symbol}>
            <SearchResult
              name={r.name}
              symbol={r.symbol}
              exchange={r.exchange}
              mic={r.mic}
            />
            {!showAdd && (
              <button
                onClick={() => {
                  setShowAdd(true);
                  setStockSymbol(r.symbol);
                  setShowSearch(false);
                }}
              >
                Add Holding
              </button>
            )}
          </div>
        ))}
      {showSearch && !extendedSearch && (
        <button
          onClick={() => {
            setExtendedSearch(true);
          }}
        >
          Extend Search
        </button>
      )}
      {!showSearch && (
        <StockData
          asset={stockdata?.name}
          symbol={stockdata?.symbol}
          date={stockdata?.date}
          currentPrice={stockdata?.price}
          exchange={stockdata?.exchange}
          currency={stockdata?.currency}
        />
      )}
      {!showSearch && showAdd && (
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
