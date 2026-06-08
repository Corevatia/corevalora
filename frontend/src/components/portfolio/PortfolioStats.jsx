import { formatPrice } from "../../lib/format";
import { convert } from "../../lib/money";

export default function PortfolioStats({
  holdings,
  rates,
  currency,
  onCurrencyChange,
  ratesLoading,
  ratesError,
}) {
  const currencies = rates.map((r) => r.exchange_currency);

  const totals = holdings.reduce(
    (acc, h) => {
      const invested = convert(h.avg_price * h.amount, h.currency, rates);

      const value = convert((h.price ?? 0) * h.amount, h.currencies, rates);

      if (invested == null || value == null) return acc;
      acc.invested += invested;
      acc.value += value;
      return acc;
    },
    {
      invested: 0,
      value: 0,
    },
  );
  const gain = totals.value - totals.invested;
  const gainColor = gain >= 0 ? "green" : "red";

  return (
    <div style={{ padding: 16, fontFamily: "system-ui" }}>
      {ratesLoading && <p>Loading...</p>}
      {ratesError && <p>ERROR</p>}
      <select
        value={currency}
        onChange={(e) => onCurrencyChange(e.target.value)}
        style={{ padding: 8 }}
      >
        {currencies.map((c) => (
          <option key={c}>{c}</option>
        ))}
      </select>
      <p>Invested: {formatPrice(totals.invested, currency)}</p>
      <p>Portfolio Value: {formatPrice(totals.value, currency)}</p>
      <p style={{ color: gainColor }}>
        Gain/Loss: {formatPrice(gain, currency)}
      </p>
    </div>
  );
}
