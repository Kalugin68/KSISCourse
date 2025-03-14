import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        """Установление соединения с сервером"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Ошибка соединения с сервером: {e}")
            return False

    def send_credentials(self, username, password):
        """Отправка логина и пароля на сервер"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            client_socket.send(f"{username};{password}".encode("utf-8"))

            response = client_socket.recv(1024).decode("utf-8")
            client_socket.close()
            return response
        except Exception as e:
            print(f"[ERROR] {e}")
            return "ERROR"
