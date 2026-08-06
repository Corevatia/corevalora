import SearchResult from "../shared/SearchResult";
import c from "../shared/card.module.css";

function ResultRow({ result, onSelect }) {
  return (
    <div className={c.card}>
      <SearchResult
        name={result.name}
        symbol={result.symbol}
        rank={result.rank}
      />
      <button
        className="bg-mist-100 hover:bg-mist-300 dark:bg-mist-700 dark:hover:bg-mist-900 text-neutral-900 dark:text-white font-bold py-2 px-4 rounded-2xl"
        onClick={() => onSelect(result.key)}
      >
        Add Holding
      </button>
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
      <h2 className="pt-0.5">SearchResults:</h2>
      {loading && <p>Loading...</p>}
      {error && <p>Error</p>}
      {!error &&
        searchdata?.map((r) => (
          <ResultRow key={r.symbol} result={r} onSelect={onSelect} />
        ))}
    </div>
  );
}
