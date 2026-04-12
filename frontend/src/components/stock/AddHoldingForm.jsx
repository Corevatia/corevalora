import StockData from "./StockData";

export default function AddHoldingForm({
  stockdata,
  onConfirm,
  amount,
  onAmountChange,
}) {
  return (
    <div>
      <StockData
        asset={stockdata?.name}
        symbol={stockdata?.symbol}
        date={stockdata?.date}
        currentPrice={stockdata?.price}
        exchange={stockdata?.exchange}
        currency={stockdata?.currency}
      />
      <div>
        <input
          value={amount}
          onChange={(e) => onAmountChange(e.target.value)}
          placeholder="Amount (e.g. 0.5)"
        />
        <button onClick={onConfirm}>Confirm</button>
      </div>
    </div>
  );
}
