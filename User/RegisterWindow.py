import customtkinter as ctk


# ====== Окно регистрации ======
class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, client):
        super().__init__()
        self.client = client

        self.__username = None
        self.__password = None
        self.__correct_password = None

        # Получаем размеры экрана и устанавливаем геометрию окна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 550
        window_height = 505
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.title("Регистрация")
        self.geometry("400x350")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Регистрация", font=("Arial", 20)).pack(pady=10)

        self.new_username_entry = ctk.CTkEntry(self.frame, placeholder_text="Придумайте логин")
        self.new_username_entry.pack(pady=5)

        self.new_password_entry = ctk.CTkEntry(self.frame, placeholder_text="Придумайте пароль", show="*")
        self.new_password_entry.pack(pady=5)

        # Фрейм для пароля и кнопки "Глаз"
        self.password_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.password_frame.pack(pady=5, fill="x")

        self.second_password_entry = ctk.CTkEntry(self.password_frame, placeholder_text="Повторите пароль", show="*")
        self.second_password_entry.pack(padx=(89, 5), pady=5, side="left")

        # Кнопка скрытия\открытия пароля
        self.show_password = False
        self.toggle_button = ctk.CTkButton(self.password_frame, text="👁", width=10, command=self.toggle_password)
        self.toggle_button.pack(side="left")

        self.register_button = ctk.CTkButton(self.frame, text="Зарегистрироваться", command=self.register_user)
        self.register_button.pack(pady=10)

        self.error_label = ctk.CTkLabel(self.frame, text="", text_color="red")
        self.error_label.pack(pady=10)

    def register_user(self):
        self.set_username(self.new_username_entry.get())
        self.set_password(self.new_password_entry.get())
        self.set_correct_password(self.second_password_entry.get())

        if not self.get_username() or not self.get_password() or not self.get_correct_password():
            self.error_label.configure(text="Введите логин и пароль!", text_color="red")
            return

        if self.get_password() == self.get_correct_password() and self.get_username():
            # Отправляем данные на сервер
            response = self.client.send_data(f"REGISTER;{self.get_username()};{self.get_password()}")

            if response == "OK":
                self.error_label.configure(text="Профиль создан!", text_color="green")
                self.client.reconnect()
                self.destroy()  # Закрываем окно регистрации
            else:
                self.error_label.configure(text="Данный аккаунт уже существует!", text_color="red")

        else:
            self.error_label.configure(text="Пароли не совпадают!", text_color="red")
            return

    def toggle_password(self):
        """Переключение видимости пароля"""
        self.show_password = not self.show_password
        self.new_password_entry.configure(show="" if self.show_password else "*")
        self.second_password_entry.configure(show="" if self.show_password else "*")

    def get_username(self):
        return self.__username
    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password
    def set_password(self, password):
        self.__password = password

    def get_correct_password(self):
        return self.__correct_password
    def set_correct_password(self, correct_password):
        self.__correct_password = correct_password
