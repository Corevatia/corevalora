const BASE_URL = "http://localhost:8000";

export async function request(path, options = {}) {
  const controller = new AbortController();
  const { timeout = 8000, signal: externalSignal, ...fetchOptions } = options;

  externalSignal?.addEventListener("abort", () => controller.abort());

  const timeoutId = setTimeout(() => controller.abort(), timeout);
  try {
    const response = await fetch(BASE_URL + path, {
      ...fetchOptions,
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error("HTTP Error " + response.status);
    }

    return response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
