import customtkinter as ctk
from UserData import UserDatabase
from tkinter import messagebox


# ====== Окно регистрации ======
class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

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

    def register_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        correct_password = self.second_password_entry.get()

        if password == correct_password and username:
            data_user_db = UserDatabase(username, password)
            if data_user_db.connect_db():
                data_user_db.create_user_db()
            else:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")

            self.destroy()

    def toggle_password(self):
        """Переключение видимости пароля"""
        self.show_password = not self.show_password
        self.new_password_entry.configure(show="" if self.show_password else "*")
        self.second_password_entry.configure(show="" if self.show_password else "*")
