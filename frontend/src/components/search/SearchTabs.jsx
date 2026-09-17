const TABS = [
  { kind: "stock", label: "Stocks" },
  { kind: "crypto", label: "Crypto" },
  { kind: "metal", label: "Metals" },
];

const base = "py-1.5 px-4 rounded-xl font-semibold";
const active = "bg-mist-700 text-white dark:bg-mist-300 dark:text-neutral-900";
const inactive =
  "bg-mist-100 hover:bg-mist-300 dark:bg-mist-900 dark:hover:bg-mist-700 text-neutral-900 dark:text-white";

export default function SearchTabs({ kind, onChange }) {
  return (
    <div className="flex justify-center gap-2">
      {TABS.map((tab) => {
        const selected = tab.kind === kind;
        return (
          <button
            key={tab.id}
            type="button"
            aria-pressed={selected}
            onClick={() => onChange(tab.kind)}
            className={`${base} ${selected ? active : inactive}`}
          >
            {tab.label}
          </button>
        );
      })}
    </div>
  );
}
