export default function SearchResult({ name, symbol, exchange, mic }) {
  return (
    <div>
      <h3>{name}</h3>
      <p>Symbol: {symbol}</p>
      <p>
        Exchange: {exchange} mic: {mic}
      </p>
    </div>
  );
}
