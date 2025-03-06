import customtkinter as ctk
from OrganizerWindow import OrganizerWindow
from RegisterWindow import RegisterWindow

# ====== Окно Авторизации ======
class AuthorizationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Авторизация")
        self.geometry("400x300")
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

        # Поле пароля
        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Пароль", show="*")
        self.password_entry.pack(pady=5)

        # Кнопка входа
        self.login_button = ctk.CTkButton(self.frame, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

        # Кнопка для скрытия/отображения пароля
        self.show_password = False
        self.toggle_button = ctk.CTkButton(self.frame, text="👁", width=10, command=self.toggle_password)
        self.toggle_button.pack(pady=5)

        self.register_button = ctk.CTkButton(self.frame, text="Регистрация", fg_color="gray",
                                             command=self.open_register)
        self.register_button.pack(pady=5)

    def login(self):
        """ Проверка логина (заглушка) и открытие основного окна """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "1234":  # Пример логина (позже можно заменить на БД)
            self.withdraw()  # Закрываем окно авторизации
            main_app = OrganizerWindow()  # Открываем основное окно
            main_app.mainloop()
        else:
            self.label.configure(text="Ошибка: неверные данные!", text_color="red")

    def toggle_password(self):
        """Переключение видимости пароля"""
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")

    def open_register(self):
        """Открытие окна регистрации"""
        register_window = RegisterWindow(self)
        register_window.grab_set()  # Делаем модальным

def main():
    app = AuthorizationWindow()
    app.mainloop()


main()