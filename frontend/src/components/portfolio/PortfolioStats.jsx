import { formatPrice } from "../../lib/format";
import { holdingTotals } from "../../lib/money";

export default function PortfolioStats({
  holdings,
  rates,
  currency,
  ratesLoading,
  ratesError,
}) {
  const totals = holdings.reduce(
    (acc, h) => {
      const { invested, value } = holdingTotals(h, rates);

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
      <div className="flex flex-col gap-2 pt-5 text-lg">
        <p>Invested: {formatPrice(totals.invested, currency)}</p>
        <p>Portfolio Value: {formatPrice(totals.value, currency)}</p>
        <p style={{ color: gainColor }}>
          Gain/Loss: {formatPrice(gain, currency)}
        </p>
      </div>
    </div>
  );
}
