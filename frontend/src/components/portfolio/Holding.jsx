export default function Holding({ asset, symbol, amount, currentPrice }) {
  const currentvalue = amount * currentPrice;
  return (
    <div>
      <h3>{asset.toUpperCase()}</h3>
      <p>Symbol: {symbol}</p>
      <p>Amount: {amount}</p>
      <p>Value: {currentvalue}$</p>
    </div>
  );
}
