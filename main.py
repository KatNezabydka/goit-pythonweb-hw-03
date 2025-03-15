import logging
import mimetypes
import urllib.parse
from collections.abc import Callable
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a"
)


class HttpHandler(BaseHTTPRequestHandler):
    BASE_PATH = Path(__file__).parent

    def do_POST(self) -> None:  # noqa: N802
        """Handle POST requests and parse the data"""
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        logging.info(f"Data parse: {data_parse}")
        data_dict = {key: value for key, value in [el.split("=") for el in data_parse.split("&")]}  # noqa: C416
        append_new_entry(data_dict)

        # Redirect to the home page
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        """Handle GET requests"""
        # HTML pages routing
        route = urllib.parse.urlparse(self.path)
        file_path = Path(self.BASE_PATH / "static" / route.path[1:])

        if route.path == "/":
            self.send_html_file("index.html")
        elif route.path == "/message":
            self.send_html_file("message.html")
        elif route.path == "/read":
            self.send_html_file("read.html")
        elif file_path.exists():
            self.send_static(path=file_path)
        else:
            self.send_html_file("error.html", HTTPStatus.NOT_FOUND)

    def send_html_file(self, filename: str, status: int = HTTPStatus.OK) -> None:
        """Send an HTML file"""
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with Path.open(self.BASE_PATH / "templates" / filename, "rb") as fd:  # type: ignore[call-overload]
            self.wfile.write(fd.read())

    def send_static(self, path: Path) -> None:
        """Send static files"""
        self.send_response(HTTPStatus.OK)
        mt = mimetypes.guess_type(path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with Path.open(path, "rb") as file:
            self.wfile.write(file.read())


def append_new_entry(new_data, filename='storage/data.json'):
    timestamp = datetime.now().isoformat()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[timestamp] = new_data

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logging.info("Data saved successfully")
        print("User data saved successfully.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")


def run(
        server_class: Callable = HTTPServer,
        handler_class: Callable = HttpHandler,
) -> None:
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    logging.info("Starting server")
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
        logging.info("Stopping server")


if __name__ == "__main__":
    run()
