export default function SearchResult({ name, symbol, exchange, mic, rank }) {
  return (
    <div>
      <h3 className="text-xl font-bold">{name}</h3>
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
