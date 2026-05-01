import { useState } from "react";
import { formatPrice } from "../../lib/format";

export default function AddHoldingForm({ data, loading, error, onConfirm }) {
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Sorry, something went wrong</p>;
  if (!data) return null;
  return (
    <AddHoldingFormReady key={data.symbol} data={data} onConfirm={onConfirm} />
  );
}

function AddHoldingFormReady({ data, onConfirm }) {
  const [amount, setAmount] = useState("");
  const [buyPrice, setBuyPrice] = useState(String(data.price));

  function handleConfirm() {
    const amt = Number(amount);
    const bp = Number(buyPrice);
    if (!Number.isFinite(amt) || amt <= 0) return;
    if (!Number.isFinite(bp) || bp <= 0) return;
    onConfirm({ amount: amt, buyPrice: bp });
  }

  return (
    <div>
      <h3>{data.name}</h3>
      <p>Symbol: {data.symbol}</p>
      <p>Market price: {formatPrice(data.price, data.currency)}</p>
      <p>Last Update: {data.date}</p>
      {data.exchange && <p>Exchange: {data.exchange}</p>}
      <div>
        <label>
          Buy price:{" "}
          <input
            type="number"
            min="0"
            step="any"
            value={buyPrice}
            onChange={(e) => setBuyPrice(e.target.value)}
          />{" "}
          {data.currency}
        </label>
      </div>
      <div>
        <input
          type="number"
          min="0"
          step="any"
          required
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="Amount (e.g. 0.5)"
        />
        <button onClick={handleConfirm}>Confirm</button>
      </div>
    </div>
  );
}
