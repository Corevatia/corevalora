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
      <p>
        Price: {currentPrice}
        {currency}
      </p>
      <p>Last Update: {date}</p>
      <p>Exchange: {exchange}</p>
    </div>
  );
}
