import { formatDateTime, formatPrice } from "../../lib/format";
import s from "./Holding.module.css";

export default function Holding({
  asset,
  customName,
  symbol,
  amount,
  unit,
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
  const perUnit = unit ? ` / ${unit}` : "";
  return (
    <div className="p-4 mb-3 border border-card-border rounded-lg bg-card-bg">
      {stale && <p className={s.stale}>Couldn't get the current price</p>}

      <div className={s.headline}>
        <h3 className={s.asset}>{customName ?? asset}</h3>
        <span className={s.value}>
          {value != null ? formatPrice(value, currency) : "—"}
        </span>
      </div>
      {customName && (
        <p className="text-sm text-neutral-500 dark:text-neutral-400">
          {asset}
        </p>
      )}
      <p className={s.gain} style={{ color: gainColor }}>
        {gain != null ? formatPrice(gain, currency) : "—"}
      </p>

      <details className={s.details}>
        <summary>Details</summary>
        <p>Symbol: {symbol}</p>
        <p>
          Amount: {amount} {unit}
        </p>
        <p>
          Avg Price: {formatPrice(avgPrice, nativeCurrency)}
          {perUnit}
        </p>
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
