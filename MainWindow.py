import customtkinter as ctk
from client import Client
import socket
from server import Server  # Мы создадим серверный класс
import time
import threading

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.server_thread = None
        self.client = None

        self.title("Подключение к серверу")
        self.geometry("400x300")

        # Поля ввода для IP-адреса и порта
        self.ip_entry = ctk.CTkEntry(self, placeholder_text="Введите IP-адрес сервера")
        self.ip_entry.pack(pady=10)
        self.ip_entry.insert(0, "127.0.0.1")  # По умолчанию локальный сервер

        self.port_entry = ctk.CTkEntry(self, placeholder_text="Введите порт сервера")
        self.port_entry.pack(pady=10)
        self.port_entry.insert(0, "2000")  # По умолчанию 12345

        # Кнопка подключения
        self.connect_button = ctk.CTkButton(self, text="Подключиться", command=self.connect_to_server)
        self.connect_button.pack(pady=20)

        # Метка для вывода ошибок
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack()

    def connect_to_server(self):
        """Попытка подключения к серверу"""
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        # Запуск сервера в фоновом потоке
        if self.server_thread is None or not self.server_thread.is_alive():
            self.server_thread = threading.Thread(target=self.start_server, args=(ip, port))
            self.server_thread.daemon = True  # чтобы поток завершился, когда приложение закрывается
            self.server_thread.start()

        my_client = Client(ip, port)

        if my_client.connect():
            try:
                # Если подключение успешно — запускаем окно авторизации
                self.status_label.configure(text="Подключение успешно!", text_color="green")
                self.after(1000, self.open_auth_window, ip, port)  # Пауза перед открытием окна авторизации

            except Exception as e:
                self.status_label.configure(text=f"Ошибка подключения: {e}", text_color="red")

    def start_server(self, ip, port):
        server = Server(ip, port)
        server.start()

    def open_auth_window(self, ip, port):
        """Открытие окна авторизации"""
        self.withdraw()  # Закрываем главное окно
        from AuthorizationWindow import AuthorizationWindow  # Импортируем только при успешном подключении
        auth_window = AuthorizationWindow()
        auth_window.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
