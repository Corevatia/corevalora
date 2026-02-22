import { request } from "../../lib/http";

export function fetchCryptoPrice(name) {
  const response = request(`/crypto/price/${name}`);
  return response;
}
export function fetchStockPrice(symbol) {
  const response = request(`/stock/price/${symbol}`);
  return response;
}
