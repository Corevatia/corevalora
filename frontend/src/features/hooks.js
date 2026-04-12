import { useEffect, useState } from "react";
import {
  fetchCryptoPrice,
  fetchStockSearch,
  fetchStockEOD,
  fetchStockSearchBackup,
  fetchCurrencyRate,
} from "./api";

export function useCryptoprice(name) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!name) return;

    const controller = new AbortController();

    fetchCryptoPrice(name, { signal: controller.signal })
      .then(setData)
      .catch((err) => {
        if (err.name !== "AbortError") console.error(err);
      });

    return () => controller.abort();
  }, [name]);
  return data;
}

export function useStockprice(symbol) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!symbol) return;

    const controller = new AbortController();

    fetchStockEOD(symbol, { signal: controller.signal })
      .then(setData)
      .catch((err) => {
        if (err.name !== "AbortError") console.error(err);
      });

    return () => controller.abort();
  }, [symbol]);
  return data;
}

export function useStockSearch(query) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!query) return;

    const controller = new AbortController();

    fetchStockSearch(query, { signal: controller.signal })
      .then(setData)
      .catch((err) => {
        if (err.name !== "AbortError") console.error(err);
      });

    return () => controller.abort();
  }, [query]);
  return data;
}

export function useStockSearchBackup(query, enabled = false) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!enabled || !query) return;

    const controller = new AbortController();

    fetchStockSearchBackup(query, { signal: controller.signal })
      .then(setData)
      .catch((err) => {
        if (err.name !== "AbortError") console.error(err);
      });

    return () => controller.abort();
  }, [enabled, query]);
  return data;
}

export function useCurrencyRate(baseCurrency) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!baseCurrency) return;

    const controller = new AbortController();

    fetchCurrencyRate(baseCurrency, { signal: controller.signal })
      .then(setData)
      .catch((err) => {
        if (err.name !== "AbortError") console.error(err);
      });

    return () => controller.abort();
  }, [baseCurrency]);
  return data;
}
