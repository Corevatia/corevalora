import { useCryptoSearch } from "../../features/hooks.js";
import ResultList from "./ResultList.jsx";

export default function CryptoResults({ query, onSelect }) {
  const { data, loading, error } = useCryptoSearch(query);

  return (
    <ResultList
      kind="crypto"
      results={data}
      loading={loading}
      error={error}
      onSelect={onSelect}
    />
  );
}
