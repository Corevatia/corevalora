import UserBadge from "./components/auth/UserBadge";
import { Dashboard } from "./pages/Dashboard";
import Login from "./pages/Login";
import { useMe } from "./features/hooks";
import ServiceUnavailable from "./pages/ServiceUnavailable";

export default function App() {
  const { user, loading, error, refetch } = useMe();

  if (loading) {
    return <div style={{ padding: 16 }}>...</div>;
  }
  if (error) {
    return <ServiceUnavailable onRetry={refetch} />;
  }
  if (!user) {
    return <Login onSuccess={refetch} />;
  }

  return (
    <>
      <Dashboard />
      <UserBadge user={user} onLogout={refetch} />
    </>
  );
}
