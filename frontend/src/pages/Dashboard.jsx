import { useState } from "react";
import Portfolio from "../components/portfolio/Portfolio";
import CryptoSearch from "../components/crypto/CryptoSearch";
import StockSearch from "../components/stock/StockSearch";
import PortfolioStats from "../components/portfolio/PortfolioStats";
import { useHoldings, useDeleteHolding } from "../features/hooks";

export function Dashboard() {
  const [mode, setMode] = useState("stock");

  const { holdings, loading, error, refetch } = useHoldings();
  const { remove } = useDeleteHolding();

  async function handleDelete(symbol) {
    try {
      await remove(symbol);
      refetch();
    } catch {
      //
    }
  }

  const items = holdings ?? [];

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
          <CryptoSearch onSaved={refetch} />
        ) : (
          <StockSearch onSaved={refetch} />
        )}
      </div>
      <div
        style={{
          width: "400px",
          overflow: "auto",
          borderLeft: "1px solid #ddd",
        }}
      >
        {loading && <p>Loading...</p>}
        {error && <p>Could not load holdings</p>}
        <Portfolio holdings={items} onDelete={handleDelete} />
      </div>
      <div
        style={{
          width: "400px",
          overflow: "auto",
          borderRight: "1px solid #ddd",
          borderLeft: "1px solid #ddd",
        }}
      >
        <PortfolioStats holdings={items} />
      </div>
    </div>
  );
}
