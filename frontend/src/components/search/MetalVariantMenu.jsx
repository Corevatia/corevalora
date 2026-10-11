const CARD = "p-4 border-card-border rounded-lg bg-card-bg";

export default function MetalVariantMenu({
  variants,
  loading,
  error,
  onPick,
  onCreate,
}) {
  if (loading) return <p className="text-center">Loading...</p>;
  if (error)
    return <p className="text-center">Could not load your holdings.</p>;

  return (
    <div className="flex flex-col gap-3">
      {variants.length > 0 && (
        <>
          <h3 className="text-lg font-bold">Add to an existing holding</h3>
          {variants.map((holding) => (
            <button
              key={holding.id}
              type="button"
              onClick={() => onPick(holding)}
              className={`${CARD} flex items-center justify-between text-left hover:bg-mist-100 dark:hover:bg-mist-900`}
            >
              <span className="text-xl font-bold">
                {holding.custom_name ?? holding.asset}
              </span>
              <span>
                {holding.amount} {holding.unit ?? "g"}
              </span>
            </button>
          ))}
        </>
      )}
      <button
        type="button"
        onClick={onCreate}
        className="bg-mist-100 hover:bg-mist-300 dark:bg-mist-700 dark:hover:bg-mist-900 text-neutral-900 dark:text-white font-bold py-2 px-4 rounded-2xl"
      >
        + Create New Holding
      </button>
    </div>
  );
}
