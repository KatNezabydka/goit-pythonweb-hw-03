import logging
import mimetypes
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a"
)

# Настройка Jinja2
TEMPLATES_PATH = Path(__file__).parent / "templates"
env = Environment(loader=FileSystemLoader(TEMPLATES_PATH), autoescape=True)


class HttpHandler(BaseHTTPRequestHandler):
    BASE_PATH = Path(__file__).parent

    def do_POST(self) -> None:
        """Обработчик POST-запросов (сохранение данных)"""
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        logging.info(f"Data parse: {data_parse}")
        data_dict = {key: value for key, value in [el.split("=") for el in data_parse.split("&")]}
        append_new_entry(data_dict)

        # Перенаправление на главную страницу
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self) -> None:
        """Обработчик GET-запросов (загрузка страниц)"""
        route = urllib.parse.urlparse(self.path)
        file_path = Path(self.BASE_PATH / "static" / route.path[1:])

        if route.path == "/":
            self.send_html_file("index.html")
        elif route.path == "/message":
            self.send_html_file("message.html")
        elif route.path == "/read":
            self.render_template("read.html", messages=load_messages())  # Новый маршрут
        elif file_path.exists():
            self.send_static(file_path)
        else:
            self.send_html_file("error.html", HTTPStatus.NOT_FOUND)

    def send_html_file(self, filename: str, status: int = HTTPStatus.OK) -> None:
        """Отправка статического HTML-файла"""
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with Path.open(self.BASE_PATH / "templates" / filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self, path: Path) -> None:
        """Отправка статических файлов"""
        self.send_response(HTTPStatus.OK)
        mt = mimetypes.guess_type(path)
        self.send_header("Content-type", mt[0] if mt else "text/plain")
        self.end_headers()
        with Path.open(path, "rb") as file:
            self.wfile.write(file.read())

    def render_template(self, template_name: str, **context) -> None:
        """Рендеринг Jinja2 шаблона"""
        template = env.get_template(template_name)
        content = template.render(context)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


def append_new_entry(new_data, filename="storage/data.json"):
    """Сохранение новых данных в JSON-файл"""
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
    except Exception as e:
        logging.error(f"Error saving data: {e}")


def load_messages(filename="storage/data.json"):
    """Загрузка сохранённых сообщений"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def run():
    """Запуск сервера"""
    server_address = ("", 3000)
    http = HTTPServer(server_address, HttpHandler)
    logging.info("Starting server")
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
        logging.info("Stopping server")


if __name__ == "__main__":
    run()
