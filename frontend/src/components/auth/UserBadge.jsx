import { useLogout } from "../../features/hooks";
import s from "./UserBadge.module.css";

export default function UserBadge({ user, onLogout }) {
  const { logout, loading } = useLogout();

  async function handleLogout() {
    try {
      await logout();
    } finally {
      onLogout();
    }
  }

  return (
    <div className={s.topRight}>
      <div className={s.badge}>
        <span style={{ fontSize: 13 }}>{user.email}</span>
        <button className={s.btn} onClick={handleLogout} disabled={loading}>
          {loading ? "..." : "Log out"}
        </button>
      </div>
    </div>
  );
}