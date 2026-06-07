import SearchResult from "../shared/SearchResult";

function ResultRow({ result, onSelect }) {
  return (
    <div>
      <SearchResult
        name={result.name}
        symbol={result.symbol}
        rank={result.rank}
      />
      <button onClick={() => onSelect(result.key)}>Add Holding</button>
    </div>
  );
}

export default function CryptoSearchResults({
  searchdata,
  loading,
  error,
  onSelect,
}) {
  return (
    <div>
      <h2>SearchResults:</h2>
      {loading && <p>Loading...</p>}
      {error && <p>Error</p>}
      {!error &&
        searchdata?.map((r) => (
          <ResultRow key={r.symbol} result={r} onSelect={onSelect} />
        ))}
    </div>
  );
}
