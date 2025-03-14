import socket
import threading
import psycopg2
from Data import UserData

class Server:
    def __init__(self, host="127.0.0.1", port=2000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[SERVER] Запущен на {self.host}:{self.port}")

        self.db = UserData.UserDatabase("123", "123")  # Объект базы данных

    def handle_client(self, client_socket):
        """Обработка запроса клиента"""
        try:
            data = client_socket.recv(1024).decode("utf-8")
            username, password = data.split(";")  # Ожидаем "логин;пароль"

            if self.db.check_user(username, password):
                client_socket.send("OK".encode("utf-8"))
            else:
                client_socket.send("FAIL".encode("utf-8"))

        except Exception as e:
            print(f"[ERROR] {e}")
            client_socket.send("ERROR".encode("utf-8"))

        finally:
            client_socket.close()

    def start(self):
        """Запуск сервера"""
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"[NEW CONNECTION] {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    server = Server()
    server.start()
