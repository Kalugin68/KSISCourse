import customtkinter as ctk
from tkcalendar import Calendar
from PIL import Image, ImageDraw


# ====== Главное окно ======
class OrganizerWindow(ctk.CTkToplevel):
    def __init__(self, master, username, password):
        super().__init__(master)

        # Получаем размеры экрана и устанавливаем геометрию окна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 550
        window_height = 505
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.__login_name = username
        self.__login_password = password

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
            "tasks": self.create_tasks_page(),
            "notes": self.create_notes_page(),
            "calendar": self.create_calendar_page(),
            "settings": self.create_settings_page()
        }
        self.add_image_with_tooltip()
        self.show_frame("tasks")  # Показываем страницу по умолчанию

    # Доступ к логину и паролю
    def get_login_name(self):
        return self.__login_name
    def get_login_password(self):
        return self.__login_password

    def show_frame(self, name):
        """Отображает нужную страницу"""
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def create_author_page(self):
        frame = ctk.CTkFrame(self.content_frame)
        ctk.CTkLabel(frame, text="Информация о профиле", font=("Arial", 18)).pack(pady=10)
        return frame

    def create_tasks_page(self):
        """Страница с задачами"""
        frame = ctk.CTkFrame(self.content_frame)
        frame.pack(fill="both", expand=True)

        self.tasks_list_label = ctk.CTkLabel(frame, text="Список задач", font=("Arial", 18))
        self.tasks_list_label.pack(pady=(10, 5))

        # Фрейм со списком задач
        self.tasks_frame = ctk.CTkScrollableFrame(frame)
        self.tasks_frame.pack(fill="both", expand=True, pady=5, padx=5)

        self.tasks = []  # Список для хранения задач

        # Фрейм для кнопок
        self.button_tasks_frame = ctk.CTkFrame(frame)
        self.button_tasks_frame.pack(fill="both", padx=5, pady=10)

        # Кнопки для работы с задачами
        self.add_task_button = ctk.CTkButton(self.button_tasks_frame, text="Добавить задачу", command=self.show_task_entry)
        self.add_task_button.grid(row=0, column=0, pady=10, padx=30)

        self.edit_task_button = ctk.CTkButton(self.button_tasks_frame, text="Редактировать задачу")
        self.edit_task_button.grid(row=0, column=1, pady=10, padx=30)

        self.task_entry_frame = None  # Фрейм для ввода задачи

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

    def show_task_entry(self):
        """Показывает поле ввода для новой задачи"""
        if self.task_entry_frame is None:
            self.task_entry_frame = ctk.CTkFrame(self.tasks_frame)
            self.task_entry_frame.pack(fill="x", pady=5)

            self.task_entry = ctk.CTkEntry(self.task_entry_frame, width=400, placeholder_text="Введите задачу...")
            self.task_entry.pack(side="left", padx=5)

            confirm_button = ctk.CTkButton(self.task_entry_frame, text="✔", width=30, command=self.add_task)
            confirm_button.pack(side="right", padx=5)

    def add_task(self):
        """Добавление новой задачи"""
        task_text = self.task_entry.get().strip()

        if task_text:
            task_frame = ctk.CTkFrame(self.tasks_frame)
            task_frame.pack(fill="x", pady=5)

            task_label = ctk.CTkLabel(task_frame, text=task_text, anchor="w")
            task_label.pack(side="left", padx=5)

            delete_button = ctk.CTkButton(task_frame, text="❌", width=30, command=lambda: self.remove_task(task_frame))
            delete_button.pack(side="right", padx=5)

            self.tasks.append(task_frame)

        # Удаляем поле ввода после добавления задачи
        if self.task_entry_frame:
            self.task_entry_frame.destroy()
            self.task_entry_frame = None

    def remove_task(self, task_frame):
        """Удаление задачи"""
        self.tasks.remove(task_frame)
        task_frame.destroy()

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
