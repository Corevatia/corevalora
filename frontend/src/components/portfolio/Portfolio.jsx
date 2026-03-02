import Holding from "../portfolio/Holding.jsx";

export default function Portfolio({ holdings, onDelete }) {
  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>Portfolio</h1>
      {holdings.map((h) => (
        <div key={h.asset}>
          <Holding
            asset={h.asset}
            symbol={h.symbol}
            amount={h.amount}
            date={h.date}
            currentPrice={h.price}
            exchange={h.exchange}
            currency={h.currency}
          />
          <button onClick={() => onDelete({ asset: h.asset })}>delete</button>
        </div>
      ))}
    </div>
  );
}
