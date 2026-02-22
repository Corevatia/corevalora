import { useState } from "react";
import { useStockprice } from "../../features/crypto/hooks";
import { SearchBar } from "../shared/SearchBar";
import { PriceCard } from "../crypto/PriceCard";

export default function StockSearch({ onAddHolding }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [amount, setAmount] = useState("");

  const data = useStockprice(query);

  function saveHolding() {
    if (!data?.symbol) return;
    const amt = Number(amount);
    if (!Number.isFinite(amt) || amt <= 0) return;
    onAddHolding({
      asset: data.symbol,
      symbol: data.symbol,
      amount: amt,
      price: Number(data.price),
    });

    setAmount("");
    setShowAdd(false);
  }
  function onKeyDown(e) {
    if (e.key === "Enter") {
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

      <PriceCard asset={data?.symbol} price={data?.price} />
      {data?.symbol && !showAdd && (
        <button onClick={() => setShowAdd(true)}>Add holding</button>
      )}

      {data?.symbol && showAdd && (
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
