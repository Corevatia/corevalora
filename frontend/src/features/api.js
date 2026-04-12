import { request } from "../lib/http";

export function fetchCryptoPrice(name, options = {}) {
  return request(`/crypto/price/${name}`, options);
}

export function fetchStockEOD(symbol, options = {}) {
  return request(`/stock/eod_price/${symbol}`, options);
}

export function fetchStockSearch(query, options = {}) {
  return request(`/stock/search/${query}`, options);
}

export function fetchStockSearchBackup(query, options = {}) {
  return request(`/stock/search/backup/${query}`, options);
}

export function fetchCurrencyRate(baseCurrency, options = {}) {
  return request(`/currency/rates/${baseCurrency}`, options);
}
