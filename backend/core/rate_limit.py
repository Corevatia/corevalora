from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


def client_key(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if user is not None:
        return f"user:{user.id}"
    return get_remote_address(request)


limiter = Limiter(key_func=client_key, key_style="endpoint")
