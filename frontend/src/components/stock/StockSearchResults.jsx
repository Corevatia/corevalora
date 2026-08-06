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
      <button
        className="bg-mist-700 hover:bg-mist-900 text-white font-bold py-2 px-4 rounded-2xl"
        onClick={() => onSelect(result.key)}
      >
        Add Holding
      </button>
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
        <div className="pt-3 text-center">
          <button
            className="bg-mist-400 hover:bg-mist-600 dark:bg-mist-900 hover:dark:bg-mist-950 text-white font-semibold py-2 px-2 rounded-xl"
            onClick={onExtend}
          >
            Extend Search
          </button>
        </div>
      )}
    </div>
  );
}
