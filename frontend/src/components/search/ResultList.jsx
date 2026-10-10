import SearchResult from "../shared/SearchResult";

function ResultRow({ result, onSelect }) {
  return (
    <div className="relative p-4 mb-3 border border-card-border rounded-lg bg-card-bg ">
      <div className="flex items-center min-h-20">
        <img
          //Logo will later be generated in the backend, for now we will use a placeholder image
          src={`https://img.logo.dev/ticker/AAPL?token=pk_IjJ81s9ESTK5bRGFRIyr5A&size=64&format=webp&retina=true&fallback=404`}
          className="absolute left-4 top-4 w-20 h-20 rounded-full"
        ></img>
        <div className="flex-1 px-24 text-center">
          <SearchResult
            name={result.name}
            symbol={result.symbol}
            rank={result.rank}
            exchange={result.exchange}
            mic={result.mic}
          />
        </div>
      </div>
      <div className="mt-1 flex justify-end">
        <button
          className="bg-mist-100 hover:bg-mist-300 dark:bg-mist-700 dark:hover:bg-mist-900 text-neutral-900 shrink-0 dark:text-white font-bold py-2 px-4 rounded-2xl"
          onClick={() => onSelect(result.key)}
        >
          Add Holding
        </button>
      </div>
    </div>
  );
}

export default function ResultList({ results, loading, error, onSelect }) {
  if (loading) return <p className="text-center">Loading...</p>;
  if (error) return <p className="text-center">Could not load results.</p>;
  if (!results || results.length === 0)
    return <p className="text-center">No results found.</p>;

  return (
    <>
      {results.map((r) => (
        <ResultRow key={r.key} result={r} onSelect={onSelect} />
      ))}
    </>
  );
}
