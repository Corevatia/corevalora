import { useMemo, useState } from "react";
import { useStockSearch, useStockSearchBackup } from "../../features/hooks";
import ResultList from "../search/ResultList";

export default function StockResults({ query, onSelect }) {
  const { extendedQuery, setExtendedQuery } = useState(null);
  const extendend = extendedQuery === query;

  const { data, loading, error } = useStockSearch(query);
  const {
    data: rawBackup,
    loading: backupLoading,
    error: backupError,
  } = useStockSearchBackup(query, extendend);

  const backup = useMemo(() => {
    const existing = new Set((data ?? []).map((r) => r.symbol));
    return (rawBackup ?? []).filter((r) => !existing.has(r.symbol));
  }, [rawBackup, data]);

  return (
    <div>
      <ResultList
        results={data}
        loading={loading}
        error={error}
        onSelect={onSelect}
      />
      {extendend ? (
        <ResultList
          results={backup}
          loading={backupLoading}
          error={backupError}
          onSelect={onSelect}
        />
      ) : (
        data &&
        !loading &&
        !error && (
          <div className="pt-3 text-center">
            <button
              className="bg-mist-400 hover:bg-mist-600 dark:bg-mist-900 hover:dark:bg-mist-950 text-white font-semibold py-2 px-2 rounded-xl"
              onClick={() => setExtendedQuery(query)}
            >
              Extend Search
            </button>
          </div>
        )
      )}
    </div>
  );
}
