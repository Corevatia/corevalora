import { useState } from "react";
import { formatDateTime, formatPrice } from "../../lib/format";

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
      <h3 className="text-xl font-bold">{data.name}</h3>
      <p>Symbol: {data.symbol}</p>
      <p>Market price: {formatPrice(data.price, data.currency)}</p>
      <p>Last Update: {formatDateTime(data.date)}</p>
      {data.exchange && <p>Exchange: {data.exchange}</p>}
      <div className="pt-3">
        <label className="font-semibold">
          Buy price:{" "}
          <input
            type="number"
            min="0"
            step="any"
            value={buyPrice}
            onChange={(e) => setBuyPrice(e.target.value)}
            className="border border-gray-300 rounded-md px-2 py-1 text-sm"
          />{" "}
          {data.currency}
        </label>
      </div>
      <div className="pt-1">
        <label className="font-semibold">
          Amount:{" "}
          <input
            type="number"
            min="0"
            step="any"
            required
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Amount (e.g. 0.5)"
            className="border border-gray-300 rounded-md px-2 py-1 text-sm"
          />
        </label>
      </div>
      <div className="pt-3 text-center">
        <button
          onClick={handleConfirm}
          className="bg-mist-100 hover:bg-mist-300 dark:bg-mist-700 dark:hover:bg-mist-900 text-neutral-900 dark:text-white font-bold py-1.5 px-5 rounded-2xl"
        >
          Confirm
        </button>
      </div>
    </div>
  );
}
