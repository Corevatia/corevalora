import { useMemo, useState } from "react";
import {
  useLogoStatus,
  useStockSearch,
  useStockSearchBackup,
} from "../../features/hooks";
import ResultList from "../search/ResultList";

const BUTTON =
  "bg-mist-400 hover:bg-mist-600 dark:bg-mist-900 hover:dark:bg-mist-950 text-white font-semibold py-2 px-2 rounded-xl";

const isUnverified = (r) => r.verified === false;

const sortByLogo = (results, withLogo) =>
  [...results].sort(
    (a, b) => (withLogo?.has(b.symbol) ?? 0) - (withLogo?.has(a.symbol) ?? 0),
  );

export default function StockResults({ query, onSelect }) {
  const [extendedQuery, setExtendedQuery] = useState(null);
  const [unverifiedQuery, setUnverifiedQuery] = useState(null);
  const extended = extendedQuery === query;
  const showUnverified = unverifiedQuery === query;

  const { data, loading, error } = useStockSearch(query);
  const {
    data: rawBackup,
    loading: backupLoading,
    error: backupError,
  } = useStockSearchBackup(query, extended);

  const backup = useMemo(() => {
    const existing = new Set((data ?? []).map((r) => r.symbol));
    return (rawBackup ?? []).filter((r) => !existing.has(r.symbol));
  }, [rawBackup, data]);

  const dataLogos = useLogoStatus((data ?? []).map((r) => r.symbol));
  const backupLogos = useLogoStatus(backup.map((r) => r.symbol));
  const allLogos = new Set([...(dataLogos ?? []), ...(backupLogos ?? [])]);

  const verifedData = sortByLogo(
    (data ?? []).filter((r) => !isUnverified(r)),
    dataLogos,
  );
  const verifiedBackup = sortByLogo(
    backup.filter((r) => !isUnverified(r)),
    backupLogos,
  );
  const unverified = sortByLogo(
    [
      ...(data ?? []).filter(isUnverified),
      ...(extended ? backup.filter(isUnverified) : []),
    ],
    allLogos,
  );

  const ready = data && !loading && !error && dataLogos;

  return (
    <div>
      <ResultList
        kind="stock"
        results={verifedData}
        loading={loading || !dataLogos}
        error={error}
        onSelect={onSelect}
      />
      {extended ? (
        <ResultList
          kind="stock"
          results={verifiedBackup}
          loading={backupLoading || !backupLogos}
          error={backupError}
          onSelect={onSelect}
        />
      ) : (
        ready && (
          <div className="pt-3 text-center">
            <button className={BUTTON} onClick={() => setExtendedQuery(query)}>
              Extend Search
            </button>
          </div>
        )
      )}
      {showUnverified ? (
        <div className="pt-3">
          <p className="mb-3 text-sm text-center text-neutral-500 dark:text-neutral-400">
            OpenFIGI couldn't confirm these tickers. Most of them are faulty
            listings, but some exchanges use tickers OpenFIGI doesn't know, so a
            real stock can end up here by mistake. Double-check the ticker and
            exchange before adding one.
          </p>
          <ResultList
            kind="stock"
            results={unverified}
            onSelect={onSelect}
            unverified
          />
        </div>
      ) : (
        ready &&
        unverified.length > 0 && (
          <div className="pt-3 text-center">
            <button
              className={BUTTON}
              onClick={() => setUnverifiedQuery(query)}
            >
              Show unverified ({unverified.length})
            </button>
          </div>
        )
      )}
    </div>
  );
}
