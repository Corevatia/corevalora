import { useState } from "react";
import UserBadge from "./components/auth/UserBadge";
import { Dashboard } from "./pages/Dashboard";
import Login from "./pages/Login";
import Search from "./pages/Search";
import { useMe } from "./features/hooks";
import ServiceUnavailable from "./pages/ServiceUnavailable";

export default function App() {
  const { user, loading, error, refetch } = useMe();
  const [view, setView] = useState("dashboard");

  if (loading) {
    return <div style={{ padding: 16 }}>...</div>;
  }
  if (error) {
    return <ServiceUnavailable onRetry={refetch} />;
  }
  if (!user) {
    return <Login onSuccess={refetch} />;
  }

  if (view === "search") {
    return <Search onClose={() => setView("dashboard")} />;
  }

  return (
    <>
      <Dashboard onAddTransaction={() => setView("search")} />
      <UserBadge user={user} onLogout={refetch} />
    </>
  );
}
