export default function Holding({
  asset,
  symbol,
  amount,
  currentPrice,
  exchange,
  currency,
}) {
  const currentvalue = amount * currentPrice;
  return (
    <div>
      <h3>{asset}</h3>
      <p>Symbol: {symbol}</p>
      <p>Amount: {amount}</p>
      <p>Value: {currentvalue}$</p>

      {exchange && <p>Exchange: {exchange}</p>}
      {currency && <p>Currency: {currency}</p>}
    </div>
  );
}
