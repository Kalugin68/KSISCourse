import customtkinter as ctk
from tkinter import messagebox
from OrganizerWindow import OrganizerWindow
from RegisterWindow import RegisterWindow
from ConnectDatabase import Database


# ====== Окно авторизации ======
class AuthorizationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Создаём объект БД
        self.db = Database()

        self.__username = None
        self.__password = None

        # Получаем размеры экрана и устанавливаем геометрию окна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 550
        window_height = 505
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.title("Авторизация")
        self.geometry("400x350")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Фрейм для элементов формы
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Заголовок
        self.label = ctk.CTkLabel(self.frame, text="Вход в органайзер", font=("Arial", 20))
        self.label.pack(pady=10)

        # Поле логина
        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Логин")
        self.username_entry.pack(pady=5)

        # Фрейм для пароля и кнопки "Глаз"
        self.password_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.password_frame.pack(pady=5, fill="x")

        # Поле пароля
        self.password_entry = ctk.CTkEntry(self.password_frame, placeholder_text="Пароль", show="*")
        self.password_entry.pack(side="left", padx=(89, 5))

        # Кнопка скрытия\открытия пароля
        self.show_password = False
        self.toggle_button = ctk.CTkButton(self.password_frame, text="👁", width=10, command=self.toggle_password)
        self.toggle_button.pack(side="left")

        # Кнопка входа
        self.login_button = ctk.CTkButton(self.frame, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

        # Кнопка регистрации
        self.register_button = ctk.CTkButton(self.frame, text="Регистрация",
                                             fg_color="gray", command=self.open_register)
        self.register_button.pack(pady=5)

        self.error_label = ctk.CTkLabel(self.frame, text="", text_color="red")
        self.error_label.pack()

    # Доступ к защищённым полям
    def get_username(self):
        return self.__username
    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password
    def set_password(self, password):
        self.__password = password

    def toggle_password(self):
        """Переключение видимости пароля"""
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")

    def login(self):
        """Проверка логина (заглушка) и открытие основного окна"""
        self.set_username(self.username_entry.get())
        self.set_password(self.password_entry.get())

        if self.db.connect_db():  # Проверяем соединение с БД
            try:
                self.db.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                                        (self.get_username(), self.get_password()))
                user = self.db.cursor.fetchone()  # Получаем запись, если она есть

                if user:
                    self.withdraw()  # Скрываем окно авторизации
                    main_app = OrganizerWindow(self, self.get_username(), self.get_password())  # Открываем главное окно
                    main_app.mainloop()

            except Exception as ex:
                messagebox.showerror("Ошибка", f"Ошибка выполнения запроса: {ex}")

            finally:
                # Закрываем соединение
                self.db.close_connection()

        else:
            # Очищаем текст ошибки
            self.error_label.configure(text="Ошибка: неверные данные!")

    def open_register(self):
        """Открытие окна регистрации"""
        register_window = RegisterWindow(self)
        register_window.grab_set()  # Делаем модальным


def main():
    app = AuthorizationWindow()
    app.mainloop()


main()
