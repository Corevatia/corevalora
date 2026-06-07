import { useCallback, useEffect, useState } from "react";
import {
  fetchCryptoPrice,
  fetchStockSearch,
  fetchStockEOD,
  fetchStockSearchBackup,
  fetchCurrencyRate,
  fetchMe,
  loginUser,
  registerUser,
  logoutUser,
  fetchHoldings,
  saveHolding,
  deleteHolding,
  fetchCryptoSearch,
} from "./api";

function useFetch(fetchFn, param, enabled = true) {
  const [state, setState] = useState({
    data: null,
    error: null,
    resolvedKey: null,
  });

  const active = Boolean(enabled && param);
  const loading = active && state.resolvedKey !== param;

  useEffect(() => {
    if (!active) return;

    const controller = new AbortController();

    fetchFn(param, { signal: controller.signal })
      .then((data) => {
        setState({ data, error: null, resolvedKey: param });
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error(err);
          setState((prev) => ({ ...prev, error: err, resolvedKey: param }));
        }
      });

    return () => controller.abort();
  }, [active, param, fetchFn]);

  return { data: state.data, loading, error: state.error };
}

function useQuery(fetchFn) {
  const [state, setState] = useState({
    data: null,
    loading: true,
    error: null,
  });
  const [reloadToken, setReloadToken] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    fetchFn({ signal: controller.signal })
      .then((data) => {
        setState({ data, loading: false, error: null });
      })
      .catch((err) => {
        if (err.name === "AbortError") return;
        console.error(err);
        setState((prev) => ({ ...prev, loading: false, error: err }));
      });

    return () => controller.abort();
  }, [reloadToken, fetchFn]);

  const refetch = useCallback(() => {
    setState((prev) => ({ ...prev, loading: true }));
    setReloadToken((n) => n + 1);
  }, []);
  return { ...state, refetch };
}

function useMutation(mutationFn) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const mutate = useCallback(
    async (...args) => {
      setLoading(true);
      setError(null);
      try {
        return await mutationFn(...args);
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [mutationFn],
  );

  return { mutate, loading, error };
}

export const useCryptoprice = (name) => useFetch(fetchCryptoPrice, name);

export const useCryptoSearch = (query) => useFetch(fetchCryptoSearch, query);

export const useStockprice = (symbol) => useFetch(fetchStockEOD, symbol);

export const useStockSearch = (query) => useFetch(fetchStockSearch, query);

export const useStockSearchBackup = (query, enabled = false) =>
  useFetch(fetchStockSearchBackup, query, enabled);

export const useCurrencyRate = (baseCurrency) =>
  useFetch(fetchCurrencyRate, baseCurrency);

export function useMe() {
  const { data, loading, error, refetch } = useQuery(fetchMe);
  return { user: data, loading, error, refetch };
}

export function useLogin() {
  const { mutate, loading, error } = useMutation(loginUser);
  return { login: mutate, loading, error };
}

export function useRegister() {
  const { mutate, loading, error } = useMutation(registerUser);
  return { register: mutate, loading, error };
}

export function useLogout() {
  const { mutate, loading, error } = useMutation(logoutUser);
  return { logout: mutate, loading, error };
}

export function useHoldings() {
  const { data, loading, error, refetch } = useQuery(fetchHoldings);
  return { holdings: data, loading, error, refetch };
}

export function useSaveHolding() {
  const { mutate, loading, error } = useMutation(saveHolding);
  return { save: mutate, loading, error };
}

export function useDeleteHolding() {
  const { mutate, loading, error } = useMutation(deleteHolding);
  return { remove: mutate, loading, error };
}
