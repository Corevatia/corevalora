import SearchResult from "./SearchResult";

export default function StockSearchResults({
  searchdata,
  loading,
  error,
  extendedloading,
  extendederror,
  extendedsearchdata,
  extendedSearch,
  showAdd,
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
          <div key={r.symbol}>
            <SearchResult
              name={r.name}
              symbol={r.symbol}
              exchange={r.exchange}
              mic={r.mic}
            />
            {!showAdd && (
              <button
                onClick={() => {
                  onSelect(r.symbol);
                }}
              >
                Add Holding
              </button>
            )}
          </div>
        ))}
      {extendedloading && <p>Loading...</p>}
      {extendederror && <p>Error</p>}
      {extendedSearch &&
        extendedsearchdata?.map((r) => (
          <div key={r.symbol}>
            <SearchResult
              name={r.name}
              symbol={r.symbol}
              exchange={r.exchange}
              mic={r.mic}
            />
            {!showAdd && (
              <button
                onClick={() => {
                  onSelect(r.symbol);
                }}
              >
                Add Holding
              </button>
            )}
          </div>
        ))}
      {!error && !extendederror && !extendedSearch && searchdata && (
        <button
          onClick={() => {
            onExtend();
          }}
        >
          Extend Search
        </button>
      )}
    </div>
  );
}
