import customtkinter as ctk
from tkcalendar import Calendar


# ====== Главное окно ======
class OrganizerWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Сетевой органайзер")
        self.geometry("800x600")
        ctk.set_appearance_mode("System")  # Тема (Light/Dark)
        ctk.set_default_color_theme("blue")  # Цветовая схема

        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Навигационная панель (левая часть)
        self.nav_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.nav_frame.pack(side="left", fill="y")

        self.nav_buttons = {
            "Задачи": ctk.CTkButton(self.nav_frame, text="Задачи", command=lambda: self.show_frame("tasks")),
            "Заметки": ctk.CTkButton(self.nav_frame, text="Заметки", command=lambda: self.show_frame("notes")),
            "Календарь": ctk.CTkButton(self.nav_frame, text="Календарь", command=lambda: self.show_frame("calendar")),
            "Настройки": ctk.CTkButton(self.nav_frame, text="Настройки", command=lambda: self.show_frame("settings"))
        }

        for btn in self.nav_buttons.values():
            btn.pack(fill="x", padx=10, pady=5)

        # Контентная область (правая часть)
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Создаем страницы
        self.frames = {
            "tasks": self.create_tasks_page(),
            "notes": self.create_notes_page(),
            "calendar": self.create_calendar_page(),
            "settings": self.create_settings_page()
        }

        self.show_frame("tasks")  # Показываем страницу по умолчанию

    def create_tasks_page(self):
        """Страница с задачами"""
        frame = ctk.CTkFrame(self.content_frame)
        ctk.CTkLabel(frame, text="Список задач", font=("Arial", 18)).pack(pady=10)
        ctk.CTkButton(frame, text="Добавить задачу").pack(pady=5)
        return frame

    def create_notes_page(self):
        """Страница с заметками"""
        frame = ctk.CTkFrame(self.content_frame)
        ctk.CTkLabel(frame, text="Заметки", font=("Arial", 18)).pack(pady=10)
        ctk.CTkTextbox(frame, width=400, height=300).pack(pady=5)
        return frame

    def create_calendar_page(self):
        """Страница с календарем"""
        frame = ctk.CTkFrame(self.content_frame)
        ctk.CTkLabel(frame, text="Календарь", font=("Arial", 18)).pack(pady=10)
        cal = Calendar(frame, selectmode="day")
        cal.pack(pady=5)
        return frame

    def create_settings_page(self):
        """Страница с настройками"""
        frame = ctk.CTkFrame(self.content_frame)
        ctk.CTkLabel(frame, text="Настройки", font=("Arial", 18)).pack(pady=10)
        return frame

    def show_frame(self, name):
        """Отображает нужную страницу"""
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)