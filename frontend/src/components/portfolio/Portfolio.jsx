import { holdingTotals } from "../../lib/money.js";
import Holding from "../portfolio/Holding.jsx";

export default function Portfolio({ holdings, rates, currency, onDelete }) {
  const rows = holdings
    .map((h) => ({ holding: h, ...holdingTotals(h, rates) }))
    .sort((a, b) => (b.value ?? -Infinity) - (a.value ?? -Infinity));
  return (
    <div style={{ padding: 12, fontFamily: "system-ui" }}>
      <h1>Portfolio</h1>
      {rows.map(({ holding: h, value, invested }) => (
        <Holding
          key={h.id}
          asset={h.asset}
          customName={h.custom_name}
          symbol={h.symbol}
          amount={h.amount}
          unit={h.unit}
          date={h.price_date}
          avgPrice={h.avg_price}
          nativeCurrency={h.currency}
          value={value}
          invested={invested}
          currency={currency}
          exchange={h.exchange}
          stale={h.stale}
          onDelete={() => onDelete(h.id)}
        />
      ))}
    </div>
  );
}
