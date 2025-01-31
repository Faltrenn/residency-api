import json
from server import RequestHandler


def get_body(rh: RequestHandler) -> dict:
    content_length = int(rh.headers.get("Content-Length", 0))
    body_data = rh.rfile.read(content_length).decode("utf-8")
    if not body_data:
        return {}

    body = json.loads(body_data)

    if not isinstance(body, dict):
        raise ValueError("Invalid body")

    return body
