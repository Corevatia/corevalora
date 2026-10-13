import { formatDateTime, formatPrice } from "../../lib/format";
const CLIENT_ID = import.meta.env.VITE_BRANDFETCH_CLIENT_ID;

export default function Holding({
  asset,
  kind,
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
  const gainColor =
    gain != null && gain >= 0 ? "text-green-600" : "text-red-600";
  const perUnit = unit ? ` / ${unit}` : "";
  return (
    <div className="p-4 mb-3 border border-card-border rounded-lg bg-card-bg">
      {stale && (
        <p className="mb-2 text-sm text-red-600">
          Couldn't get the current price
        </p>
      )}
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3">
        {kind === "stock" && (
          <img
            src={`https://cdn.brandfetch.io/ticker/${symbol}?c=${CLIENT_ID}`}
            alt="Logo by Brandfetch"
            className="w-12 h-12 rounded-full"
          />
        )}
        {kind === "crypto" && (
          <img
            src={`https://cdn.brandfetch.io/crypto/${symbol}?c=${CLIENT_ID}`}
            alt="Logo by Brandfetch"
            className="w-12 h-12 rounded-full"
          />
        )}
        {kind === "metal" && (
          // backend will eventually provide logos for metals as well
          <img className="w-12 h-12 rounded-full" />
        )}
        <div className="min-w-0 self-start text-center">
          <h3 className="text-xl font-bold leading-tight wrap-break-words">
            {customName ?? asset}
          </h3>
          {customName && (
            <p className="text-sm text-neutral-500 dark:text-neutral-400">
              {asset}
            </p>
          )}
        </div>
        <div className="self-start pt-1 text-right whitespace-nowrap">
          <p className="font-semibold">
            {value != null ? formatPrice(value, currency) : "—"}
          </p>
          <p className={`text-sm font-semibold ${gainColor}`}>
            {gain != null ? formatPrice(gain, currency) : "—"}
          </p>
        </div>
      </div>

      <div className="mt-2 flex items-start justify-between gap-3">
        <details className="text-sm">
          <summary className="cursor-pointer select-none text-card-border">
            Details
          </summary>
          <div className="mt-1 space-y-1">
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
          </div>
        </details>
        <button
          className="shrink-0 cursor-pointer px-3 py-1 text-sm border border-card-border rounded-md text-red-600 hover:bg-red-600 hover:text-white"
          onClick={onDelete}
        >
          delete
        </button>
      </div>
    </div>
  );
}
