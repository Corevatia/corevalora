import Holding from "../portfolio/Holding.jsx";

export default function Portfolio({ holdings, onDelete }) {
  return (
    <div style={{ padding: 12, fontFamily: "system-ui" }}>
      <h1>Portfolio</h1>
      {holdings.map((h) => (
        <div key={h.id}>
          <Holding
            asset={h.asset}
            symbol={h.symbol}
            amount={h.amount}
            date={h.price_date}
            avgPrice={h.avg_price}
            currentPrice={h.price}
            exchange={h.exchange}
            currency={h.currency}
            stale={h.stale}
          />
          <button onClick={() => onDelete(h.symbol)}>delete</button>
        </div>
      ))}
    </div>
  );
}
