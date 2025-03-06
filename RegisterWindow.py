import customtkinter as ctk


# ====== Окно регистрации ======
class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Регистрация")
        self.geometry("400x350")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Регистрация", font=("Arial", 20)).pack(pady=10)

        self.new_username_entry = ctk.CTkEntry(self.frame, placeholder_text="Придумайте логин")
        self.new_username_entry.pack(pady=5)

        self.new_password_entry = ctk.CTkEntry(self.frame, placeholder_text="Придумайте пароль", show="*")
        self.new_password_entry.pack(pady=5)

        self.register_button = ctk.CTkButton(self.frame, text="Зарегистрироваться", command=self.register)
        self.register_button.pack(pady=10)

    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if username and password:
            print(f"Пользователь {username} зарегистрирован!")  # Заглушка, тут можно подключить БД
            self.destroy()