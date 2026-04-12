import SearchResult from "./SearchResult";

export default function StockSearchResults({
  searchdata,
  extendedsearchdata,
  extendedSearch,
  showAdd,
  onExtend,
  onSelect,
}) {
  return (
    <div>
      <h2>SearchResults:</h2>
      {searchdata?.map((r) => (
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
      {!extendedSearch && (
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
