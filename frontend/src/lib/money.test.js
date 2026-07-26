import { describe, it, expect } from "vitest";

import { convert } from "./money";

describe("convert", () => {
  const rates = [
    { exchange_currency: "EUR", rate: 0.5 },
    { exchange_currency: "CHF", rate: 0.8 },
  ];

  it("converts the amount using the matching rate", () => {
    expect(convert(100, "EUR", rates)).toBe(200); // 100 / 0.5
  });

  it("returns null when the currency is not in the rates", () => {
    expect(convert(100, "GBP", rates)).toBeNull();
  });
});
