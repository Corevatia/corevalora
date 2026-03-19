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

    fetchCryptoPrice(name).then(setData).catch(console.error);
  }, [name]);
  return data;
}
export function useStockprice(symbol) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!symbol) return;

    fetchStockEOD(symbol).then(setData).catch(console.error);
  }, [symbol]);
  return data;
}
export function useStockSearch(query) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!query) return;

    fetchStockSearch(query).then(setData).catch(console.error);
  }, [query]);
  return data;
}
export function useStockSearchBackup(query, enabled = false) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!enabled || !query) return;

    fetchStockSearchBackup(query).then(setData).catch(console.error);
  }, [enabled, query]);
  return data;
}
export function useCurrencyRate(baseCurrency) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!baseCurrency) return;

    fetchCurrencyRate(baseCurrency).then(setData).catch(console.error);
  }, [baseCurrency]);
  return data;
}
