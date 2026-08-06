import Portfolio from "../components/portfolio/Portfolio";
import CryptoSearch from "../components/crypto/CryptoSearch";
import StockSearch from "../components/stock/StockSearch";
import PortfolioStats from "../components/portfolio/PortfolioStats";
import {
  useHoldings,
  useDeleteHolding,
  useCurrencyRate,
} from "../features/hooks";
import { useLocalStorage } from "../hooks/useLocalStorage";

const column = "min-w-0 flex-1 max-w-100 overflow-y-auto";

export function Dashboard() {
  const [mode, setMode] = useLocalStorage("cv:mode", "stock");
  const [currency, setCurrency] = useLocalStorage("cv:currency", "EUR");

  const { holdings, loading, error, refetch } = useHoldings();
  const { remove } = useDeleteHolding();
  const {
    data: ratedata,
    loading: ratesLoading,
    error: ratesError,
  } = useCurrencyRate(currency);

  const rates = ratedata?.rates ?? [];

  async function handleDelete(id) {
    try {
      await remove(id);
      refetch();
    } catch {
      //
    }
  }

  const items = holdings ?? [];

  return (
    <div className="flex h-screen justify-center divide-x divide-neutral-300 dark:divide-neutral-700">
      <div className={`${column} p-1.5`}>
        <div className="flex items-center gap-3 justify-content ">
          <h2 className="text-3xl font-extrabold p-2">Dashboard</h2>
        </div>
        <div className="pt-9 flex justify-center">
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="p-1.5 px-7 text-lg"
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
      <div className={column}>
        {loading && <p className="p-4">Loading...</p>}
        {error && <p className="p-4">Could not load holdings</p>}
        <Portfolio
          holdings={items}
          rates={rates}
          currency={currency}
          onDelete={handleDelete}
        />
      </div>
      <div className={column}>
        <PortfolioStats
          holdings={items}
          rates={rates}
          currency={currency}
          onCurrencyChange={setCurrency}
          ratesLoading={ratesLoading}
          ratesError={ratesError}
        />
      </div>
    </div>
  );
}
