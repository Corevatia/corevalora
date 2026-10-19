const CLIENT_ID = import.meta.env.VITE_BRANDFETCH_CLIENT_ID;

export const stockLogoUrl = (symbol) =>
  `https://cdn.brandfetch.io/ticker/${symbol}/fallback/404?c=${CLIENT_ID}`;

export const cryptoLogoUrl = (symbol) =>
  `https://cdn.brandfetch.io/crypto/${symbol}?c=${CLIENT_ID}`;
