from http.server import HTTPServer
from sys import argv
from server import RequestHandler


if __name__ == "__main__":
    if len(argv) < 3 or not argv[2].isnumeric():
        print("WRONG USAGE!")
        print("server.py ip port")
        exit(1)

    RequestHandler.initialize()
    server = HTTPServer((argv[1], int(argv[2])), RequestHandler)
    print(f"Server started at {argv[1]}:{argv[2]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
