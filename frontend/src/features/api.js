import { request } from "../lib/http";

export function fetchCryptoPrice(name) {
  const response = request(`/crypto/price/${name}`);
  return response;
}

export function fetchStockEOD(symbol) {
  const response = request(`/stock/eod_price/${symbol}`);
  return response;
}
export function fetchStockSearch(query) {
  const response = request(`/stock/search/${query}`);
  return response;
}
export function fetchStockSearchBackup(query) {
  const response = request(`/stock/search/backup/${query}`);
  return response;
}
export function fetchCurrencyRate(baseCurrency) {
  const response = request(`/currency/rates/${baseCurrency}`);
  return response;
}
