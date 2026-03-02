export default function StockData({
  asset,
  symbol,
  date,
  currentPrice,
  exchange,
  currency,
}) {
  return (
    <div>
      <h3>{asset}</h3>
      <p>Symbol: {symbol}</p>
      <p>Price: {currentPrice}$</p>
      <p>Last Update: {date}</p>
      <p>Exchange: {exchange}</p>
      <p>Currency: {currency}</p>
    </div>
  );
}
