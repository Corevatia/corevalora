import { useState } from "react";
import { useStockinfo, useStockprice } from "../../features/hooks";
import { SearchBar } from "../shared/SearchBar";
import { PriceCard } from "../crypto/PriceCard";

export default function StockSearch({ onAddHolding }) {
  const [inputValue, setInputValue] = useState("");
  const [query, setQuery] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [amount, setAmount] = useState("");

  const pricedata = useStockprice(query);
  const infodata = useStockinfo(query, pricedata?.exchange);

  function saveHolding() {
    console.debug(pricedata.exchange);
    console.debug(infodata.name);
    if (!pricedata?.symbol) return;
    const amt = Number(amount);
    if (!Number.isFinite(amt) || amt <= 0) return;
    onAddHolding({
      asset: infodata.name,
      symbol: pricedata.symbol,
      amount: amt,
      price: Number(pricedata.price),
      exchange: pricedata.exchange,
      currency: infodata.currency,
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

      <PriceCard asset={pricedata?.symbol} price={pricedata?.price} />
      {pricedata?.symbol && !showAdd && (
        <button onClick={() => setShowAdd(true)}>Add holding</button>
      )}

      {pricedata?.symbol && showAdd && (
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
