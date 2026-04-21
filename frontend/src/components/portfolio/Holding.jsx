import { formatPrice } from "../../lib/format";
import s from "./Holding.module.css";

export default function Holding({
  asset,
  symbol,
  amount,
  date,
  currentPrice,
  exchange,
  currency,
}) {
  const currentvalue = amount * currentPrice;
  return (
    <div className={s.card}>
      <h3>{asset}</h3>
      <p>Symbol: {symbol}</p>
      <p>Amount: {amount}</p>
      <p>Value:{formatPrice(currentvalue, currency)}</p>
      <p>Last Update: {date}</p>
      {exchange && <p>Exchange: {exchange}</p>}
      <p>Currency: {currency}</p>
    </div>
  );
}
