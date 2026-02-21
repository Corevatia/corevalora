import { useCryptoprice } from "../../features/crypto/hooks.js";
import { PriceCard } from "./PriceCard.jsx";
import { SearchBar } from "./SearchBar.jsx";
import { useState } from "react";


export default function CryptoSearch({onAddHolding}) {
  const [inputValue, setInputValue] = useState("")
  const [query, setQuery] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [amount, setAmount] = useState("");

  const data = useCryptoprice(query);

  function saveHolding() {
    if (!data?.asset) return;
    const amt = Number(amount);
    if (!Number.isFinite(amt) || amt <= 0) return;

    onAddHolding({asset: data.asset, symbol: data.symbol, amount: amt, price: Number(data.priceUsd)})
    
    setAmount("");
    setShowAdd(false);
  }
  function onKeyDown(e)
  {
    if (e.key === "Enter")
    {
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

      <PriceCard asset={data?.asset} price={data?.priceUsd} />
              {data?.asset && !showAdd && (
          <button onClick={() => setShowAdd(true)}>Add holding</button>
        )}

        {data?.asset && showAdd && (
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