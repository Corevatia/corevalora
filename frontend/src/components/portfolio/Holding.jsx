import { formatDateTime, formatPrice } from "../../lib/format";
import s from "./Holding.module.css";

export default function Holding({
  asset,
  symbol,
  amount,
  date,
  avgPrice,
  currentPrice,
  exchange,
  currency,
}) {
  const invested = amount * avgPrice;
  const currentvalue = amount * currentPrice;
  const gain = currentvalue - invested;
  const gainColor = gain >= 0 ? "green" : "red";
  return (
    <div className={s.card}>
      <h3>{asset}</h3>
      <p>Symbol: {symbol}</p>
      <p>Amount: {amount}</p>
      <p>Avg Price: {formatPrice(avgPrice, currency)}</p>
      <p>Value:{formatPrice(currentvalue, currency)}</p>
      <p style={{ color: gainColor }}>
        Gain/Loss: {formatPrice(gain, currency)}
      </p>
      <p>Last Update: {formatDateTime(date)}</p>
      {exchange && <p>Exchange: {exchange}</p>}
    </div>
  );
}
