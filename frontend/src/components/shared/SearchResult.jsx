export default function SearchResult({ name, symbol, exchange, mic, rank }) {
  return (
    <div>
      <h3>{name}</h3>
      <p>Symbol: {symbol}</p>
      {rank && <p>Rank: {rank}</p>}
      {exchange && (
        <p>
          Exchange: {exchange} mic: {mic}
        </p>
      )}
    </div>
  );
}
