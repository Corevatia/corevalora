import { useState } from "react";
import { METAL_UNITS } from "../../lib/units.js";

const INPUT = "border border-gray-300 rounded-md px-2 py-1 text-sm";

function sameName(a, b) {
  return a.trim().toLowerCase() === b.trim().toLowerCase();
}

export default function NewMetalHolding({ variants, onSubmit }) {
  const [customName, setCustomName] = useState("");
  const [unit, setUnit] = useState("g");

  const name = customName.trim();

  const taken =
    name !== "" &&
    variants.some((holding) => sameName(holding.custom_name ?? "", name));

  function handleSubmit(e) {
    e.preventDefault();
    if (name === "" || taken) return;
    onSubmit({ customName: name, unit });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <h3 className="text-lg font-bold">New Metal Holding</h3>
      <label className="flex flex-col gap-1 font-semibold">
        Name
        <input
          type="text"
          required
          autoFocus
          maxLength={255}
          value={customName}
          onChange={(e) => setCustomName(e.target.value)}
          placeholder="e.g. Kruggerand"
          className={INPUT}
        />
      </label>
      <label className="flex flex-col gap-1 font-semibold">
        Unit
        <select
          value={unit}
          onChange={(e) => setUnit(e.target.value)}
          className={INPUT}
        >
          {METAL_UNITS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
      {taken && <p>You already have a holding with that name.</p>}

      <div className="pt-2 text-center">
        <button
          type="submit"
          disabled={name === "" || taken}
          className="bg-mist-100 hover:bg-mist-300 dark:bg-mist-700 dark:hover:bg-mist-900 text-neutral-900 dark:text-white font-bold py-1.5 px-5 rounded-2xl disabled:opacity-50"
        >
          Continue
        </button>
      </div>
    </form>
  );
}
