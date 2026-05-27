import { useState } from "react";
import { useLogin, useRegister } from "../features/hooks";
import s from "./Login.module.css";

function getAuthErrorMessage(error) {
  if (!error) return null;
  switch (error.status) {
    case 401:
      return "Email or password wrong";
    case 409:
      return "This email is already registered";
    case 429:
      return "Too many attempts, please, wait a moment";
    case undefined:
      return "Connection to server failed";
    default:
      return "Something went wrong. please try again";
  }
}

export default function Login({ onSuccess }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { login, loading: loginLoading, error: loginError } = useLogin();
  const {
    register,
    loading: registerLoading,
    error: registerError,
  } = useRegister();

  const loading = loginLoading || registerLoading;
  const error = mode === "login" ? loginError : (registerError ?? loginError);

  async function onSubmit(e) {
    e.preventDefault();
    try {
      if (mode === "register") {
        await register({ email, password });
      }
      await login({ email, password });
      onSuccess();
    } catch {
      //
    }
  }

  return (
    <div className={s.page}>
      <div className={s.card}>
        <h2 style={{ margin: 0 }}>
          {mode === "login" ? "Login" : "Create Account"}
        </h2>

        <form onSubmit={onSubmit} className={s.form}>
          <input
            type="email"
            placeholder="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoFocus
            className={s.input}
          />
          <input
            type="password"
            placeholder="password (at least 8 characters)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            className={s.input}
          />

          {error && (
            <div style={{ color: "crimson", fontSize: 13 }}>
              {getAuthErrorMessage(error)}
            </div>
          )}

          <button type="submit" className={s.btnPrimary} disabled={loading}>
            {loading ? "..." : mode === "login" ? "Login" : "Register"}
          </button>
        </form>

        <button
          type="button"
          className={s.btnLink}
          onClick={() => setMode(mode === "login" ? "register" : "login")}
        >
          {mode === "login"
            ? "No account? Register"
            : "Already have an account? Login"}
        </button>
      </div>
    </div>
  );
}
