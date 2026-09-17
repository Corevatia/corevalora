import SearchResult from "../shared/SearchResult";
import c from "../shared/card.module.css";

function ResultRow({ result, onSelect }) {
  return (
    <div className={c.card}>
      <SearchResult
        name={result.name}
        symbol={result.symbol}
        rank={result.rank}
        exchange={result.exchange}
        mic={result.mic}
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

export default function ResultList({ results, loading, error, onSelect }) {
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Could not load results.</p>;
  if (!results || results.length === 0) return <p>No results found.</p>;

  return (
    <>
      {results.map((r) => (
        <ResultRow key={r.key} result={r} onSelect={onSelect} />
      ))}
    </>
  );
}
