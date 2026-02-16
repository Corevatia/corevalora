
export async function fetchCryptoPrice(name) {
  const response = await fetch(`http://localhost:8000/crypto/price/${name}`);

  if (!response.ok) {
    throw new Error("HTTP Error " + response.status);
  }

  const data = await response.json();
  return data;
}