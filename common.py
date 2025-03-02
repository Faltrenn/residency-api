from http import HTTPMethod
from typing import List
from server import RequestHandler
from enum import Enum

from utils import get_body


class Roles(Enum):
    ADMIN = "Admin"
    TEACHER = "Professor"
    RESIDENT = "Resident"

    @staticmethod
    def get_role(role: str) -> "Roles | None":
        match (role):
            case "Admin":
                return Roles.ADMIN
            case "Professor":
                return Roles.TEACHER
            case "Residente":
                return Roles.RESIDENT
        return None

    @staticmethod
    def get_role_title(role: "Roles") -> str:
        match (role):
            case Roles.ADMIN:
                return "Admin"
            case Roles.TEACHER:
                return "Professor"
            case Roles.RESIDENT:
                return "Residente"

    @staticmethod
    def all() -> List["Roles"]:
        return list(Roles)


def route(path: str, method: HTTPMethod):
    def decorator(func):
        setattr(func, "api", (path, method))
        return func

    return decorator


def middleware(allowedRoles: list[Roles]):
    def decorator(func):
        def wrapper(*args):
            if not args:
                raise AssertionError("No positional arguments provided")

            rh = args[0]

            if not isinstance(rh, RequestHandler):
                raise ValueError("First argument is not a RequestHandler object", rh)

            if not "token" in rh.headers:
                raise ValueError("Missing token")

            from routes.login import getRoleByToken

            role = getRoleByToken(rh.headers["token"])

            if not role:
                raise ValueError("Invalid Role")

            if role not in allowedRoles:
                raise PermissionError("Unauthorized")

            return func(*args)

        return wrapper

    return decorator


def body_keys_needed(keys_needed: list[str]):
    def decorator(func):
        def wrapper(*args):
            if not args:
                raise AssertionError("No positional arguments provided")

            rh = args[0]

            if not isinstance(rh, RequestHandler):
                raise ValueError("First argument is not a RequestHandler object")

            body = get_body(rh)

            for kn in keys_needed:
                if kn not in body:
                    raise ValueError(f"Missing {kn} in body")

            return func(*args, body=body)

        return wrapper

    return decorator
