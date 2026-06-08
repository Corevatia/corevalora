export function convert(amount, fromCurrency, rates) {
  const match = rates.find((r) => r.exchange_currency === fromCurrency);
  if (!match) return null;
  return amount / match.rate;
}
