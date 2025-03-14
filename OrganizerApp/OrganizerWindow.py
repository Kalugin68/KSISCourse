import customtkinter as ctk
from tkcalendar import Calendar
from PIL import Image, ImageDraw
from OrganizerApp import TasksPage


# ====== Главное окно ======
class OrganizerWindow(ctk.CTkToplevel):
    def __init__(self, username):
        super().__init__()

        # Получаем размеры экрана и устанавливаем геометрию окна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 550
        window_height = 505
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.__login_name = username

        self.title("Сетевой органайзер")
        self.geometry("800x600")
        ctk.set_appearance_mode("System")  # Тема (Light/Dark)
        ctk.set_default_color_theme("green")  # Цветовая схема

        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Навигационная панель (левая часть)
        self.nav_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.nav_frame.pack(side="left", fill="y")

        # Загрузка и форматирование изображения
        self.image_author = Image.open("Images/author.jpg")
        self.rounded_image_author = self.round_image(self.image_author, 1320)
        self.image_author_tk = ctk.CTkImage(size=(80, 80), light_image=self.rounded_image_author,
                                            dark_image=self.rounded_image_author)

        # Добавляем изображение в CTkLabel
        self.image_author_label = ctk.CTkLabel(self.nav_frame, text="", image=self.image_author_tk)
        self.image_author_label.pack(padx=10, pady=5)

        self.login_label = ctk.CTkLabel(self.nav_frame, text=self.get_login_name(), font=("Arial", 14))
        self.login_label.pack(padx=10, pady=5)

        self.nav_buttons = {
            "Задачи": ctk.CTkButton(self.nav_frame, text="📋 Задачи", command=lambda: self.show_frame("tasks")),
            "Заметки": ctk.CTkButton(self.nav_frame, text="📝 Заметки", command=lambda: self.show_frame("notes")),
            "Календарь": ctk.CTkButton(self.nav_frame, text="📅 Календарь", command=lambda: self.show_frame("calendar")),
            "Настройки": ctk.CTkButton(self.nav_frame, text="⚙️ Настройки", command=lambda: self.show_frame("settings"))
        }

        for btn in self.nav_buttons.values():
            btn.pack(fill="x", padx=10, pady=5)

        # Контентная область (правая часть)
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Создаем страницы
        self.frames = {
            "author": self.create_author_page(),
            "tasks": TasksPage.TasksPage(self.content_frame).create_tasks_page(),
            "notes": self.create_notes_page(),
            "calendar": self.create_calendar_page(),
            "settings": self.create_settings_page()
        }
        self.add_image_with_tooltip()
        self.show_frame("tasks")  # Показываем страницу по умолчанию

    # Доступ к логину и паролю
    def get_login_name(self):
        return self.__login_name

    def show_frame(self, name):
        """Отображает нужную страницу"""
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def create_author_page(self):
        frame = ctk.CTkFrame(self.content_frame)
        ctk.CTkLabel(frame, text="Информация о профиле", font=("Arial", 18)).pack(pady=10)
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

    def add_image_with_tooltip(self):
        # Привязываем функции к событиям клика на картинку и наведения курсора
        self.image_author_label.bind("<Enter>", self.on_hover)  # Изменение при наведении
        self.image_author_label.bind("<Leave>", self.on_leave)  # Возвращение к исходному состоянию
        self.image_author_label.bind("<Button-1>", self.show_tooltip)  # Показать всплывающую подсказку при нажатии

        # Переменная для хранения ссылки на всплывающую подсказку
        self.tooltip = None

    def show_tooltip(self, event):
        # Функция для открытия информации о профиле

        self.show_frame("author")

    def on_hover(self, event):
        # Функция для изменения визуального состояния при наведении

        self.image_author_label.configure(cursor="hand2")  # изменение курсора

    def on_leave(self, event):
        # Функция для возврата к исходному состоянию

        self.image_author_label.configure(cursor="")  # курсор по умолчанию

    def round_image(self, image_main, radius):
        # Конвертируем изображение в формат RGBA (с альфа-каналом для прозрачности)
        image_main = image_main.convert("RGBA")
        width, height = image_main.size

        # Создаем маску с закругленными углами
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=255)

        # Добавляем маску к изображению
        image_main.putalpha(mask)

        return image_main
