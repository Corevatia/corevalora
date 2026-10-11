export const GRAMS_PER_TROY_OUNCE = 31.1034768;

export const METAL_UNITS = [
  { value: "g", label: "Gram (g)" },
  { value: "toz", label: "Troy Ounce (oz t)" },
];

const GRAMS_PER_UNIT = {
  g: 1,
  toz: GRAMS_PER_TROY_OUNCE,
};

export function gramsPerUnit(unit) {
  return GRAMS_PER_UNIT[unit] ?? 1;
}

export function unitPrice(pricePerGram, unit) {
  return pricePerGram * gramsPerUnit(unit);
}
