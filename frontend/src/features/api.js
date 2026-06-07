import { request } from "../lib/http";

//crypto
export function fetchCryptoPrice(name, options = {}) {
  return request(`/crypto/price/${name}`, options);
}
export function fetchCryptoSearch(query, options = {}) {
  return request(`/crypto/search/${query}`, options);
}

//stock
export function fetchStockEOD(symbol, options = {}) {
  return request(`/stock/eod_price/${symbol}`, options);
}

export function fetchStockSearch(query, options = {}) {
  return request(`/stock/search/${query}`, options);
}

export function fetchStockSearchBackup(query, options = {}) {
  return request(`/stock/search/backup/${query}`, options);
}

//currency
export function fetchCurrencyRate(baseCurrency, options = {}) {
  return request(`/currency/rates/${baseCurrency}`, options);
}

//auth
export async function fetchMe(options = {}) {
  try {
    return await request(`/auth/me`, options);
  } catch (err) {
    if (err.status === 401) return null;
    throw err;
  }
}

export function loginUser({ email, password }, options = {}) {
  return request(`/auth/login`, {
    ...options,
    method: "POST",
    json: { email, password },
  });
}

export function registerUser({ email, password }, options = {}) {
  return request(`/auth/register`, {
    ...options,
    method: "POST",
    json: { email, password },
  });
}

export function logoutUser(options = {}) {
  return request(`/auth/logout`, { ...options, method: "POST" });
}

//portfolio
export function fetchHoldings(options = {}) {
  return request(`/portfolio/holdings`, options);
}

export function saveHolding(
  { key, asset, symbol, kind, amount, buy_price },
  options = {},
) {
  return request(`/portfolio/holdings`, {
    ...options,
    method: "POST",
    json: { key, asset, symbol, kind, amount, buy_price },
  });
}

export function deleteHolding(id, options = {}) {
  return request(`/portfolio/holdings/${id}`, {
    ...options,
    method: "DELETE",
  });
}
