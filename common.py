from http import HTTPMethod
import functools
from server import RequestHandler
from utils import get_body


def route(path: str, method: HTTPMethod):
    def decorator(func):
        setattr(func, "api", (path, method))
        return func

    return decorator


def middleware(allowedRoles: list[str]):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            from routes.login import getRoleByToken

            if not args:
                raise AssertionError("No positional arguments provided")

            rh: RequestHandler = args[0]

            if not "token" in rh.headers:
                raise ValueError("Missing token")

            role = getRoleByToken(rh.headers["token"])

            if role not in allowedRoles:
                raise PermissionError("Unauthorized")
            print("middleware")
            func(*args)

        return wrapper

    return decorator
