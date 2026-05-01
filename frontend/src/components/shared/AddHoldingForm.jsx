import { formatPrice } from "../../lib/format";

export default function AddHoldingForm({
  data,
  loading,
  error,
  amount,
  onAmountChange,
  onConfirm,
}) {
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Sorry, something went wrong</p>;
  if (!data) return null;

  return (
    <div>
      <h3>{data.name}</h3>
      <p>Symbol: {data.symbol}</p>
      <p>Price: {formatPrice(data.price, data.currency)}</p>
      <p>Last Update: {data.date}</p>
      {data.exchange && <p>Exchange: {data.exchange}</p>}
      <div>
        <input
          type="number"
          min="0"
          step="any"
          required
          value={amount}
          onChange={(e) => onAmountChange(e.target.value)}
          placeholder="Amount (e.g. 0.5)"
        />
        <button onClick={onConfirm}>Confirm</button>
      </div>
    </div>
  );
}
