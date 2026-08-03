class CoreValoraError(Exception):
    """Base class for every exception this application raises itself."""


class UpstreamError(CoreValoraError):
    """An external provider could not answer the request."""


class UpstreamUnavailable(UpstreamError):
    """Network failure or server error (5xx) at the provider."""


class UpstreamTimeout(UpstreamError):
    """The provider did not answer within the timeout."""


class ProviderRejected(UpstreamError):
    """The provider refuses this specific request but is reachable."""


class AssetNotFound(CoreValoraError):
    """The requested symbol / asset does not exist at the provider."""


class HoldingNotFound(CoreValoraError):
    """No holding with that id belongs to the current user."""


class UnknownCurrency(CoreValoraError):
    """The requested currency is missing from the exchange rate data."""
