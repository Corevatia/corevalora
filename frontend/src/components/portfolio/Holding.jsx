import { formatDateTime, formatPrice } from "../../lib/format";
import s from "./Holding.module.css";
import c from "../shared/card.module.css";

export default function Holding({
  asset,
  symbol,
  amount,
  date,
  avgPrice,
  nativeCurrency,
  value,
  invested,
  currency,
  exchange,
  stale,
  onDelete,
}) {
  const gain = value != null && invested != null ? value - invested : null;
  const gainColor = gain != null && gain >= 0 ? "green" : "red";
  return (
    <div className={c.card}>
      {stale && <p className={s.stale}>Couldn't get the current price</p>}

      <div className={s.headline}>
        <h3 className={s.asset}>{asset}</h3>
        <span className={s.value}>
          {value != null ? formatPrice(value, currency) : "—"}
        </span>
      </div>
      <p className={s.gain} style={{ color: gainColor }}>
        {gain != null ? formatPrice(gain, currency) : "—"}
      </p>

      <details className={s.details}>
        <summary>Details</summary>
        <p>Symbol: {symbol}</p>
        <p>Amount: {amount}</p>
        <p>Avg Price: {formatPrice(avgPrice, nativeCurrency)}</p>
        <p>Last Update: {formatDateTime(date)}</p>
        {exchange && <p>Exchange: {exchange}</p>}
      </details>
      <div className={s.footer}>
        <button className={s.delete} onClick={onDelete}>
          delete
        </button>
      </div>
    </div>
  );
}
