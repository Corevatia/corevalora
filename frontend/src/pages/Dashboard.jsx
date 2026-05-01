import { useState } from "react";
import Portfolio from "../components/portfolio/Portfolio";
import CryptoSearch from "../components/crypto/CryptoSearch";
import StockSearch from "../components/stock/StockSearch";
import PortfolioStats from "../components/portfolio/PortfolioStats";

export function Dashboard() {
  const [holdings, setHoldings] = useState([]);
  const [mode, setMode] = useState("stock");

  function addHolding({
    asset,
    symbol,
    amount,
    date,
    price,
    buyPrice,
    exchange,
    currency,
  }) {
    setHoldings((prev) => {
      const existing = prev.find((h) => h.asset === asset);
      if (!existing) {
        return [
          ...prev,
          {
            asset,
            symbol,
            amount,
            date,
            price,
            avgPrice: buyPrice,
            exchange,
            currency,
          },
        ];
      }
      return prev.map((h) => {
        if (h.asset !== asset) return h;
        const newAmount = h.amount + amount;
        const newAvgPrice =
          (h.amount * h.avgPrice + amount * buyPrice) / newAmount;
        return {
          ...h,
          amount: newAmount,
          avgPrice: newAvgPrice,
          price,
          date,
        };
      });
    });
  }

  function deleteHolding(asset) {
    setHoldings((prev) => prev.filter((h) => h.asset !== asset));
  }

  return (
    <div style={{ display: "flex", height: "100vh", justifyContent: "center" }}>
      <div
        style={{ padding: 16, width: "400px", borderLeft: "1px solid #ddd" }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
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
          <CryptoSearch onAddHolding={addHolding} />
        ) : (
          <StockSearch onAddHolding={addHolding} />
        )}
      </div>
      <div
        style={{
          width: "400px",
          overflow: "auto",
          borderLeft: "1px solid #ddd",
        }}
      >
        <Portfolio holdings={holdings} onDelete={deleteHolding} />
      </div>
      <div
        style={{
          width: "400px",
          overflow: "auto",
          borderRight: "1px solid #ddd",
          borderLeft: "1px solid #ddd",
        }}
      >
        <PortfolioStats holdings={holdings} />
      </div>
    </div>
  );
}
