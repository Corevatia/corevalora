import { useState } from "react";
import { useCurrencyRate } from "../../features/hooks";
export default function PortfolioStats({ holdings }) {
  const [selectedCurrency, setSelectedCurrency] = useState("EUR");

  const ratedata = useCurrencyRate(selectedCurrency);

  const currencies = ratedata?.rates.map((r) => r.exchange_currency) || [];

  let value = 0;
  holdings.map((h) => {
    if (!ratedata) return <p>Lädt...</p>;
    const currencyrate = ratedata.rates.find(
      (r) => r.exchange_currency === h.currency,
    );
    if (!currencyrate) return null;
    value = value + (h.price * h.amount) / currencyrate.rate;
  });
  return (
    <div>
      <select
        value={selectedCurrency}
        onChange={(e) => setSelectedCurrency(e.target.value)}
        style={{ padding: 8 }}
      >
        {currencies.map((c) => (
          <option key={c}>{c}</option>
        ))}
      </select>
      <p>
        Portfolio Value:{value}
        {selectedCurrency}
      </p>
    </div>
  );
}
