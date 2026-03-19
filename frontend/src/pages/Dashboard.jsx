import { useState } from "react";
import Portfolio from "../components/portfolio/Portfolio";
import CryptoSearch from "../components/crypto/CryptoSearch";
import StockSearch from "../components/stock/StockSearch";
import PortfolioStats from "../components/portfolio/PorfolioStats";

export function Dashboard() {
  const [holdings, setHolding] = useState([]);
  const [mode, setMode] = useState("stock");

  function AddHolding({
    asset,
    symbol,
    amount,
    date,
    price,
    exchange,
    currency,
  }) {
    const amt = Number(amount);
    const prc = Number(price);
    setHolding((prev) => {
      const existing = prev.find((h) => h.asset === asset);
      if (!existing) {
        return [
          ...prev,
          {
            asset: asset,
            symbol: symbol,
            amount: amt,
            date: date,
            price: prc,
            exchange: exchange,
            currency: currency,
          },
        ];
      }

      const newamount = existing.amount + amt;

      return prev.map((h) =>
        h.asset === asset ? { ...h, amount: newamount } : h,
      );
    });
  }
  function DeleteHolding({ asset }) {
    setHolding((prev) => prev.filter((h) => h.asset !== asset));
  }

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ padding: 16 }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            marginBottom: 16,
          }}
        >
          <h2 style={{ margin: 0 }}>Dashboard</h2>

          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            style={{ padding: 8 }}
          >
            <option value="crypto">Crypto</option>
            <option value="stock">Stocks</option>
          </select>
        </div>
        {mode === "crypto" ? (
          <CryptoSearch onAddHolding={AddHolding} />
        ) : (
          <StockSearch onAddHolding={AddHolding} />
        )}
      </div>
      <div
        style={{
          width: "400px",
          overflow: "auto",
          borderRight: "1px solid #ddd",
          borderLeft: "1px solid #ddd",
        }}
      >
        <Portfolio holdings={holdings} onDelete={DeleteHolding} />
      </div>
      <div
        style={{
          width: "400px",
          overflow: "auto",
          borderRight: "1px solid #ddd",
          borderLeft: "1px solid #ddd",
        }}
      >
        <PortfolioStats holdings={holdings}></PortfolioStats>
      </div>
    </div>
  );
}
