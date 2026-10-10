export default function SearchResult({ name, symbol, exchange, mic, rank }) {
  return (
    <div className="flex flex-col items-center gap-1 p-2 rounded-lg">
      <h3 className="text-2xl font-bold">{name}</h3>
      <div className="flex items-center gap-4">
        <div>
          <p>Symbol: {symbol}</p>
          {rank && <p>Rank: {rank}</p>}
          {exchange && (
            <div>
              <p>Exchange: {exchange}</p>
              <p> mic: {mic}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
