import Portfolio from "../components/portfolio/Portfolio";
import PortfolioStats from "../components/portfolio/PortfolioStats";
import {
  useHoldings,
  useDeleteHolding,
  useCurrencyRate,
} from "../features/hooks";
import { useLocalStorage } from "../hooks/useLocalStorage";

export function Dashboard({ onAddTransaction }) {
  const [currency, setCurrency] = useLocalStorage("cv:currency", "EUR");

  const { holdings, loading, error, refetch } = useHoldings();
  const { remove } = useDeleteHolding();
  const {
    data: ratedata,
    loading: ratesLoading,
    error: ratesError,
  } = useCurrencyRate(currency);

  const rates = ratedata?.rates ?? [];
  const currencies = rates.map((r) => r.exchange_currency);

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
    <div className=" gap-2 p-2">
      <select
        className="fixed top-4 left-4"
        value={currency}
        onChange={(e) => setCurrency(e.target.value)}
      >
        {currencies.map((c) => (
          <option key={c}>{c}</option>
        ))}
      </select>
      <div className="flex justify-center">
        <div className="flex w-full max-w-xl flex-col p-4 pb-24">
          <h2 className="text-center p-2 text-4xl font-extrabold">Dashboard</h2>
          <PortfolioStats
            holdings={items}
            rates={rates}
            currency={currency}
            ratesLoading={ratesLoading}
            ratesError={ratesError}
          />
          <div className="border-t border-neutral-300 dark:border-neutral-700">
            {loading && <p className="p-4">Loading...</p>}
            {error && <p className="p-4">Could not load holdings</p>}
            <Portfolio
              holdings={items}
              rates={rates}
              currency={currency}
              onDelete={handleDelete}
            />
          </div>
        </div>

        <button
          type="button"
          aria-label="Add transaction"
          onClick={onAddTransaction}
          className="fixed right-6 bottom-6 flex h-14 w-14 items-center justify-center rounded-full bg-mist-700 text-3xl text-white shadow-lg hover:bg-mist-900 dark:bg-mist-300 dark:text-neutral-900 dark:hover:bg-mist-100"
        >
          +
        </button>
      </div>
    </div>
  );
}
