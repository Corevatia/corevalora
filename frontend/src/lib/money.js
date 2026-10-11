import { unitPrice } from "./units.js";

export function convert(amount, fromCurrency, rates) {
  const match = rates.find((r) => r.exchange_currency === fromCurrency);
  if (!match) return null;
  return amount / match.rate;
}

export function holdingTotals(holding, rates) {
  const market = unitPrice(holding.price ?? 0, holding.unit);
  return {
    value: convert(market * holding.amount, holding.currency, rates),
    invested: convert(
      holding.avg_price * holding.amount,
      holding.currency,
      rates,
    ),
  };
}
