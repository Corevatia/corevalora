import { useState } from "react";
import {
  useMe,
  useLogin,
  useRegister,
  useLogout,
} from "../../features/hooks";
import s from "./AuthMenu.module.css";

export default function AuthMenu() {
  const { user, loading: meLoading, refetch } = useMe();
  const [open, setOpen] = useState(false);

  if (meLoading) {
    return <div className={s.topRight}>...</div>;
  }

  if (!user) {
    return (
      <>
        <div className={s.topRight}>
          <button className={s.btn} onClick={() => setOpen(true)}>
            Login
          </button>
        </div>
        {open && (
          <AuthModal
            onClose={() => setOpen(false)}
            onSuccess={() => {
              setOpen(false);
              refetch();
            }}
          />
        )}
      </>
    );
  }

  return (
    <div className={s.topRight}>
      <UserBadge user={user} onLogout={refetch} />
    </div>
  );
}

function AuthModal({ onClose, onSuccess }) {
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
  const error =
    mode === "login" ? loginError : registerError ?? loginError;

  async function onSubmit(e) {
    e.preventDefault();
    try {
      if (mode === "register") {
        await register({ email, password });
      }
      await login({ email, password });
      onSuccess();
    } catch {
      // error-State
    }
  }

  return (
    <div className={s.overlay} onClick={onClose}>
      <div className={s.modal} onClick={(e) => e.stopPropagation()}>
        <h3 style={{ margin: 0 }}>
          {mode === "login" ? "Login" : "Create Account"}
        </h3>

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
              {error.message}
            </div>
          )}

          <button type="submit" className={s.btnPrimary} disabled={loading}>
            {loading
              ? "..."
              : mode === "login"
                ? "Login"
                : "Register"}
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

        <button type="button" className={s.btnLink} onClick={onClose}>
          Cancel
        </button>
      </div>
    </div>
  );
}

function UserBadge({ user, onLogout }) {
  const { logout, loading } = useLogout();

  async function handleLogout() {
    try {
      await logout();
    } finally {
      onLogout();
    }
  }

  return (
    <div className={s.badge}>
      <span style={{ fontSize: 13 }}>{user.email}</span>
      <button className={s.btn} onClick={handleLogout} disabled={loading}>
        {loading ? "..." : "Log out"}
      </button>
    </div>
  );
}