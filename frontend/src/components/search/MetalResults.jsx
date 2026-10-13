import { useMetals } from "../../features/hooks.js";
import ResultList from "./ResultList.jsx";

function matches(metal, query) {
  const q = query.toLowerCase();
  return (
    metal.name.toLowerCase().includes(q) ||
    metal.symbol.toLowerCase().includes(q)
  );
}

export default function MetalResults({ query, onSelect }) {
  const { metals, loading, error } = useMetals();
  const results = metals?.filter((m) => matches(m, query));

  return (
    <ResultList
      kind="metal"
      results={results}
      loading={loading}
      error={error}
      onSelect={onSelect}
    />
  );
}
