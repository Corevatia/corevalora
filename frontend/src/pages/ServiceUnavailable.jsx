import s from "./ServiceUnavailable.module.css";

export default function ServiceUnavailable({ onRetry }) {
  return (
    <div className={s.page}>
      <div className={s.card}>
        <h2 style={{ margin: 0 }}>Service unavailable</h2>
        <p className={s.text}>
          We can't reach the server right now. This is on our side, not yours.
          Please try again in a moment.
        </p>
        {onRetry && (
          <button type="button" className={s.btnPrimary} onClick={onRetry}>
            Retry
          </button>
        )}
      </div>
    </div>
  );
}
