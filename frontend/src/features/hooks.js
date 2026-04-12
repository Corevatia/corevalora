import { useEffect, useState } from "react";
import {
  fetchCryptoPrice,
  fetchStockSearch,
  fetchStockEOD,
  fetchStockSearchBackup,
  fetchCurrencyRate,
} from "./api";

function useFetch(fetchFn, param, enabled = true) {
  const [state, setState] = useState({
    data: null,
    error: null,
    resolvedKey: null,
  });

  const active = Boolean(enabled && param);
  const loading = active && state.resolvedKey !== param;

  useEffect(() => {
    if (!active) return;

    const controller = new AbortController();

    fetchFn(param, { signal: controller.signal })
      .then((data) => {
        setState({ data, error: null, resolvedKey: param });
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error(err);
          setState((prev) => ({ ...prev, error: err, resolvedKey: param }));
        }
      });

    return () => controller.abort();
  }, [active, param, fetchFn]);

  return { data: state.data, loading, error: state.error };
}

export const useCryptoprice = (name) => useFetch(fetchCryptoPrice, name);

export const useStockprice = (symbol) => useFetch(fetchStockEOD, symbol);

export const useStockSearch = (query) => useFetch(fetchStockSearch, query);

export const useStockSearchBackup = (query, enabled = false) =>
  useFetch(fetchStockSearchBackup, query, enabled);

export const useCurrencyRate = (baseCurrency) =>
  useFetch(fetchCurrencyRate, baseCurrency);
