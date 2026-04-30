const BASE_URL = "http://localhost:8000";

export async function request(path, options = {}) {
  const controller = new AbortController();
  const {
    timeout = 8000,
    signal: externalSignal,
    json,
    headers,
    ...fetchOptions
  } = options;

  externalSignal?.addEventListener("abort", () => controller.abort());

  const finalOptions = {
    ...fetchOptions,
    headers: { ...(headers ?? {}) },
    credentials: "include",
    signal: controller.signal,
  };

  if (json !== undefined) {
    finalOptions.body = JSON.stringify(json);
    finalOptions.headers["Content-Type"] = "application/json";
  }

  const timeoutId = setTimeout(() => controller.abort(), timeout);
  try {
    const response = await fetch(BASE_URL + path, finalOptions);

    if (!response.ok) {
      const error = new Error("HTTP Error " + response.status);
      error.status = response.status;
      throw error;
    }

    if (response.status === 204) return null;
    return response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
