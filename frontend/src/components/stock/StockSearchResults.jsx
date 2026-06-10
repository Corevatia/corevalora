import SearchResult from "../shared/SearchResult";
import c from "../shared/card.module.css";

function ResultRow({ result, onSelect }) {
  return (
    <div className={c.card}>
      <SearchResult
        name={result.name}
        symbol={result.symbol}
        exchange={result.exchange}
        mic={result.mic}
      />
      <button onClick={() => onSelect(result.key)}>Add Holding</button>
    </div>
  );
}

export default function StockSearchResults({
  searchdata,
  loading,
  error,
  extendedloading,
  extendederror,
  extendedsearchdata,
  extendedSearch,
  onExtend,
  onSelect,
}) {
  return (
    <div>
      <h2>SearchResults:</h2>
      {loading && <p>Loading...</p>}
      {error && <p>Error</p>}
      {!error &&
        searchdata?.map((r) => (
          <ResultRow key={r.key} result={r} onSelect={onSelect} />
        ))}
      {extendedloading && <p>Loading...</p>}
      {extendederror && <p>Error</p>}
      {extendedSearch &&
        extendedsearchdata?.map((r) => (
          <ResultRow key={r.key} result={r} onSelect={onSelect} />
        ))}
      {!error && !extendederror && !extendedSearch && searchdata && (
        <button onClick={onExtend}>Extend Search</button>
      )}
    </div>
  );
}
