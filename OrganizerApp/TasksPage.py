import customtkinter as ctk
from Data import TasksData
from tkinter import messagebox


class TasksPage:
    def __init__(self, parent):
        """Создаем менеджер задач внутри переданного родительского виджета"""
        self.parent = parent
        self.tasks = []  # Список для хранения задач
        self.task_entry_frame = None  # Фрейм для ввода задачи

    def create_tasks_page(self):
        """Страница с задачами"""
        frame = ctk.CTkFrame(self.parent)
        frame.pack(fill="both", expand=True)

        self.tasks_list_label = ctk.CTkLabel(frame, text="Список задач", font=("Arial", 18))
        self.tasks_list_label.pack(pady=(10, 5))

        # Фрейм со списком задач
        self.tasks_frame = ctk.CTkScrollableFrame(frame)
        self.tasks_frame.pack(fill="both", expand=True, pady=5, padx=5)

        # Фрейм для кнопок
        self.button_tasks_frame = ctk.CTkFrame(frame)
        self.button_tasks_frame.pack(fill="both", padx=5, pady=10)

        # Кнопки для работы с задачами
        self.add_task_button = ctk.CTkButton(self.button_tasks_frame, text="Добавить задачу",
                                             command=self.show_task_entry)
        self.add_task_button.grid(row=0, column=0, pady=10, padx=30)

        self.edit_task_button = ctk.CTkButton(self.button_tasks_frame, text="Редактировать задачу")
        self.edit_task_button.grid(row=0, column=1, pady=10, padx=30)

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

        data_tasks_db = TasksData.TasksDatabase(task_text)
        if data_tasks_db.connect_db():
            data_tasks_db.create_tasks_db()
            data_tasks_db.add_task(3, task_text)
        else:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")


    def remove_task(self, task_frame):
        """Удаление задачи"""
        self.tasks.remove(task_frame)
        task_frame.destroy()
