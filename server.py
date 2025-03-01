from http.server import BaseHTTPRequestHandler
from http import HTTPMethod, HTTPStatus
import json
import re
import importlib


class RequestHandler(BaseHTTPRequestHandler):
    routes = {}

    @classmethod
    def initialize(cls):
        methods = (
            HTTPMethod.GET,
            HTTPMethod.POST,
            HTTPMethod.PUT,
            HTTPMethod.DELETE,
        )

        import routes

        modules_names = [name for name in dir(routes) if not name.startswith("__")]
        functions = [
            f
            for module_name in modules_names
            for f in importlib.import_module(f"routes.{module_name}").__dict__.values()
            if hasattr(f, "api")
        ]

        cls.routes = {
            m: {
                attr[0]: f
                for f in functions
                if (attr := getattr(f, "api")) and attr[1] == m
            }
            for m in methods
        }

    def set_headers(
        self,
        status: HTTPStatus,
        message: str | None = None,
        data: dict | list | None = None,
    ):
        self.send_response(status, message)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "token, Content-Type")
        if data:
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf8"))
            return
        self.end_headers()

    def run_routes(self, method: HTTPMethod):
        # TODO: Handle erros and make right return code
        for k, v in RequestHandler.routes[method].items():
            if re.search(k, self.path):
                try:
                    v(self)
                except ValueError as ve:
                    self.set_headers(HTTPStatus.BAD_REQUEST, data={"error": str(ve)})
                except PermissionError as pe:
                    self.set_headers(HTTPStatus.UNAUTHORIZED, data={"error": str(pe)})
                except BrokenPipeError:
                    print("Client disconnected before get response.")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    self.set_headers(
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        data={"error": "Internal server error"},
                    )
                return
        self.set_headers(HTTPStatus.NOT_FOUND)

    def do_OPTIONS(self):
        self.set_headers(HTTPStatus.NO_CONTENT)

    def do_GET(self):
        self.run_routes(HTTPMethod.GET)

    def do_POST(self):
        self.run_routes(HTTPMethod.POST)

    def do_PUT(self):
        self.run_routes(HTTPMethod.PUT)

    def do_DELETE(self):
        self.run_routes(HTTPMethod.DELETE)
