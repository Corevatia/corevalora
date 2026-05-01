import { useState } from "react";
import { useCurrencyRate } from "../../features/hooks";
import { formatPrice } from "../../lib/format";

export default function PortfolioStats({ holdings }) {
  const [selectedCurrency, setSelectedCurrency] = useState("EUR");

  const { data: ratedata, loading, error } = useCurrencyRate(selectedCurrency);

  const rates = ratedata?.rates ?? [];
  const currencies = rates.map((r) => r.exchange_currency);

  const totals = holdings.reduce(
    (acc, h) => {
      const currencyrate = rates.find(
        (r) => r.exchange_currency === h.currency,
      );
      if (!currencyrate) return acc;
      acc.invested += (h.avgPrice * h.amount) / currencyrate.rate;
      acc.value += (h.price * h.amount) / currencyrate.rate;
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
      {loading && <p>Loading...</p>}
      {error && <p>ERROR</p>}
      <select
        value={selectedCurrency}
        onChange={(e) => setSelectedCurrency(e.target.value)}
        style={{ padding: 8 }}
      >
        {currencies.map((c) => (
          <option key={c}>{c}</option>
        ))}
      </select>
      <p>Invested: {formatPrice(totals.invested, selectedCurrency)}</p>
      <p>Portfolio Value: {formatPrice(totals.value, selectedCurrency)}</p>
      <p style={{ color: gainColor }}>
        Gain/Loss: {formatPrice(gain, selectedCurrency)}
      </p>
    </div>
  );
}
