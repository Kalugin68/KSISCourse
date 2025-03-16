import customtkinter as ctk
import re


class TasksPage:
    def __init__(self, parent):
        """Создаем менеджер задач внутри переданного родительского виджета"""
        self.parent = parent
        self.tasks = []  # Список для хранения задач
        self.task_entry_frame = None  # Фрейм для ввода задачи
        self.task_texts = {}  # Словарь для хранения оригинальных текстов задач

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

            # Ограничиваем количество символов, например, 100 символов
            self.task_entry = ctk.CTkEntry(self.task_entry_frame, width=400, placeholder_text="Введите задачу...",
                                           validate="key",
                                           validatecommand=(self.parent.register(self.validate_input), '%P'))
            self.task_entry.pack(side="left", padx=5)

            confirm_button = ctk.CTkButton(self.task_entry_frame, text="✔", width=30, command=self.add_task)
            confirm_button.pack(side="right", padx=5)

    def validate_input(self, value):
        """Функция для ограничения количества символов (макс. 100 символов)"""
        return len(value) <= 100  # Ограничиваем до 100 символов

    def add_task(self):
        """Добавление новой задачи"""
        task_text = self.task_entry.get().strip()

        if task_text:
            task_frame = ctk.CTkFrame(self.tasks_frame)
            task_frame.pack(fill="x", pady=5)

            # Метка с текстом задачи
            task_label = ctk.CTkLabel(task_frame, text=task_text, anchor="w", font=("Arial", 14, "normal"))
            task_label.pack(side="left", padx=5, fill="x", expand=True)

            # 🔹 Сохраняем оригинальный текст в словаре
            self.task_texts[task_label] = task_text

            # Кнопка удаления
            delete_button = ctk.CTkButton(task_frame, text="❌", width=30,
                                          command=lambda: self.remove_task(task_frame, task_label))
            delete_button.pack(side="right", padx=5)

            # Кнопка редактирования
            edit_button = ctk.CTkButton(task_frame, text="✏", width=30,
                                        command=lambda: self.edit_task(task_label, task_frame, edit_button,
                                                                       status_dropdown))
            edit_button.pack(side="right", padx=5)

            # Выпадающий список для выбора состояния
            status_var = ctk.StringVar(value="Добавь статус")
            status_options = ["Не выполнено", "В процессе", "Выполнено"]
            status_dropdown = ctk.CTkComboBox(task_frame, values=status_options, variable=status_var, state="readonly",
                                              command=lambda s: self.update_task_status(task_label, status_var))
            status_dropdown.pack(side="right", padx=5)

            self.tasks.append(task_frame)

        # Удаляем поле ввода после добавления задачи
        if self.task_entry_frame:
            self.task_entry_frame.destroy()
            self.task_entry_frame = None

    def edit_task(self, task_label, task_frame, edit_button, status_dropdown):
        """Редактирование задачи"""
        task_text = task_label.cget("text")  # Получаем текущий текст задачи

        # Убираем значок статуса (если он есть)
        clean_text = re.sub(r" [✅⏳❌]+$", "", task_text)

        # Создаём поле ввода на месте задачи
        edit_entry = ctk.CTkEntry(task_frame, width=400)
        edit_entry.insert(0, clean_text)  # Заполняем текущим текстом
        edit_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Ограничиваем ввод в поле редактирования до 100 символов
        edit_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_input), '%P'))

        # Кнопка подтверждения изменений
        self.confirm_button = ctk.CTkButton(task_frame, text="✔", width=30,
                                            command=lambda: self.confirm_edit_task(task_label, edit_entry, edit_button,
                                                                                   status_dropdown))
        self.confirm_button.pack(side="right", padx=5)

        # Скрываем старый текст задачи и кнопку редактирования
        task_label.pack_forget()
        edit_button.pack_forget()
        status_dropdown.pack_forget()

    def confirm_edit_task(self, task_label, edit_entry, edit_button, status_dropdown):
        """Сохранение отредактированной задачи"""
        new_text = edit_entry.get().strip()

        if new_text:
            # Сохраняем обновленный текст без значка в словарь
            self.task_texts[task_label] = new_text

            # Получаем текущий статус
            current_status = status_dropdown.get()

            # Восстанавливаем статусный символ
            status_symbol = " ❌" if current_status == "Не выполнено" else \
                " ⏳" if current_status == "В процессе" else \
                    " ✅" if current_status == "Выполнено" else ""

            # Обновляем текст задачи с сохранением статуса
            task_label.configure(text=new_text + status_symbol, font=("Arial", 14, "normal"))

        task_label.pack(side="left", padx=5, fill="x", expand=True)  # Показываем снова
        edit_button.pack(side="right", padx=5)  # Возвращаем кнопку редактирования
        status_dropdown.pack(side="right", padx=5)  # Возвращаем выбор состояния
        edit_entry.destroy()  # Убираем поле ввода
        self.confirm_button.destroy()

    def update_task_status(self, task_label, status_var):
        """Обновление состояния задачи (меняет отображение в зависимости от статуса)"""
        status = status_var.get()

        # 🔹 Получаем оригинальный текст из словаря
        task_text = self.task_texts.get(task_label, task_label.cget("text"))

        # Обновляем текст с новым статусом
        if status == "Выполнено":
            task_label.configure(font=("Arial", 14, "normal"), text=task_text + " ✅", text_color="Green")
        elif status == "В процессе":
            task_label.configure(font=("Arial", 14, "normal"), text=task_text + " ⏳", text_color="Orange")
        elif status == "Не выполнено":
            task_label.configure(font=("Arial", 14, "normal"), text=task_text + " ❌", text_color="Red")

    def remove_task(self, task_frame, task_label):
        """Удаление задачи"""
        self.tasks.remove(task_frame)
        self.task_texts.pop(task_label, None)  # 🔹 Удаляем текст из словаря
        task_frame.destroy()
