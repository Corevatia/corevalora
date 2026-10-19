import logging

from core.config import settings
from core.errors import AssetNotFound, UpstreamError
from models.stock import SearchResult
from services.providers.openfigi_client import OpenFigiClient

logger = logging.getLogger(__name__)

client = OpenFigiClient(api_key=settings.OPENFIGI_API_KEY)

# MarketStack MICs that OpenFIGI only knows under another code
MIC_ALIASES = {
    "XJPX": "XTKS",
    "XMIL": "MTAA",
}

EXCH_CODE_INSTEAD_OF_MIC = {"XNAS": "US"}


def normalize_for_figi(ticker: str, mic: str) -> tuple[str, str]:
    figi_mic = MIC_ALIASES.get(mic, mic)

    if "." in ticker:
        base = ticker.rpartition(".")[0].replace("-", "")
    else:
        base = ticker.replace("-", "/")
    if figi_mic == "XHKG":
        base = base.lstrip("0") or "0"
    return base, figi_mic


def _needs_figi_check(symbol: str) -> bool:
    # Preferred shares (BAC-P-L) are named after the issue on OpenFIGI
    # ("BAC 7.25 PERP L"), so they can't be checked by ticker
    return symbol.count("-") < 2


def build_figi_job(ticker: str, mic: str) -> dict:
    job = {"idType": "TICKER", "idValue": ticker}
    if mic in EXCH_CODE_INSTEAD_OF_MIC:
        job["exchCode"] = EXCH_CODE_INSTEAD_OF_MIC[mic]
    else:
        job["micCode"] = mic
    return job


def mark_with_figi(
    results: list[SearchResult], mode: str
) -> tuple[list[SearchResult], bool]:
    if mode == "off":
        return results, True

    checkable = []
    for i, r in enumerate(results):
        if _needs_figi_check(r.symbol):
            checkable.append(i)
        elif mode == "verbose":
            logger.info(
                f"OpenFIGI skipped {r.symbol} @ {r.mic} (preferred share notation"
            )

    if not checkable:
        return results, True

    jobs = [
        build_figi_job(*normalize_for_figi(results[i].symbol, results[i].mic))
        for i in checkable
    ]

    try:
        mapped = client.map_tickers(jobs)
    except (UpstreamError, AssetNotFound) as e:
        logger.warning(f"OpenFIGI check failed, returning unmarked results: {e}")
        return results, False

    if len(mapped) != len(checkable):
        logger.warning(
            f"OpenFIGI returned {len(mapped)} results for {len(checkable)} jobs,"
            " returning unmarked results"
        )
        return results, False

    marked = list(results)
    for i, job, entry in zip(checkable, jobs, mapped):
        result = results[i]
        checked = f"{job['idValue']} @ {job.get('micCode') or job['exchCode']}"
        if "data" in entry:
            verified = True
        elif "error" in entry:
            logger.warning(
                f"OpenFIGI rejected {checked}, leaving {result.symbol} unmarked: "
                f"{entry['error']}"
            )
            continue
        else:
            verified = False
            if mode == "verbose":
                logger.info(
                    f"OpenFIGI marked {result.symbol} @ {result.mic} unverified "
                    f"(checked as {checked})"
                )
        marked[i] = result.model_copy(update={"verified": verified})

    return marked, True
