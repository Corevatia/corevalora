import { convert } from "../../lib/money.js";
import Holding from "../portfolio/Holding.jsx";

export default function Portfolio({ holdings, rates, currency, onDelete }) {
  const rows = holdings
    .map((h) => ({
      holding: h,
      value: convert((h.price ?? 0) * h.amount, h.currency, rates),
      invested: convert(h.avg_price * h.amount, h.currency, rates),
    }))
    .sort((a, b) => (b.value ?? -Infinity) - (a.value ?? -Infinity));
  return (
    <div style={{ padding: 12, fontFamily: "system-ui" }}>
      <h1>Portfolio</h1>
      {rows.map(({ holding: h, value, invested }) => (
        <Holding
          key={h.id}
          asset={h.asset}
          symbol={h.symbol}
          amount={h.amount}
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
