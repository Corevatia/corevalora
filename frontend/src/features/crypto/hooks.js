import { useEffect, useState } from "react";
import { fetchCryptoPrice, fetchStockPrice } from "./api";

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

    fetchStockPrice(symbol).then(setData).catch(console.error);
  }, [symbol]);
  return data;
}
