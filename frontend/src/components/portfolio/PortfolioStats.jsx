import { useState } from "react";
import { useCurrencyRate } from "../../features/hooks";
import { formatPrice } from "../../lib/format";

export default function PortfolioStats({ holdings }) {
  const [selectedCurrency, setSelectedCurrency] = useState("EUR");

  const { data: ratedata, loading, error } = useCurrencyRate(selectedCurrency);

  const rates = ratedata?.rates ?? [];
  const currencies = rates.map((r) => r.exchange_currency);

  const value = holdings.reduce((sum, h) => {
    const currencyrate = rates.find((r) => r.exchange_currency === h.currency);
    if (!currencyrate) return sum;
    return sum + (h.price * h.amount) / currencyrate.rate;
  }, 0);

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
      <p>Portfolio Value: {formatPrice(value, selectedCurrency)}</p>
    </div>
  );
}
