import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_POST(self):
        c_len = int(self.headers.get("Content-Length"))
        client_data = self.rfile.read(c_len)
        client_data = client_data.decode()

        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "application/json")  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        response_data = {"data": client_data}
        print(client_data)
        self.wfile.write(bytes(json.dumps(response_data), "utf-8"))  # Тело ответа

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        with open("list.json", "r") as json_file:
            json_data = json.load(json_file)

        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "application/json")  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(bytes(json.dumps(json_data), "utf-8"))  # Тело ответа


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрам в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
