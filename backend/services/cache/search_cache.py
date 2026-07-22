from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from core.config import settings
from db.models import SearchCache

TTL_SECONDS = 3600 * settings.SEARCH_CACHE_TTL_HOURS


def _normalize(query: str) -> str:
    return query.strip().lower()


def read_search(db, kind, query) -> SearchCache | None:
    return db.execute(
        select(SearchCache).where(
            SearchCache.kind == kind,
            SearchCache.query == _normalize(query),
        )
    ).scalar_one_or_none()


def is_search_fresh(cached) -> bool:
    age = (datetime.now(UTC) - cached.cached_at).total_seconds()
    return age < TTL_SECONDS


def upsert_search(db: Session, *, kind: str, query: str, results: list) -> None:
    stmt = insert(SearchCache).values(
        kind=kind,
        query=_normalize(query),
        results=results,
        cached_at=datetime.now(UTC),
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["kind", "query"],
        set_={
            "results": stmt.excluded.results,
            "cached_at": stmt.excluded.cached_at,
        },
    )
    db.execute(stmt)
    db.commit()


def delete_expired_search(db: Session) -> int:
    cutoff = datetime.now(UTC) - timedelta(seconds=TTL_SECONDS)
    result = db.execute(delete(SearchCache).where(SearchCache.cached_at < cutoff))
    db.commit()
    return result.rowcount
