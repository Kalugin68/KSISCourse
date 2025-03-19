import customtkinter as ctk
import re


class TasksPage:
    def __init__(self, parent, client, user_id):
        """Создаем менеджер задач внутри переданного родительского виджета"""
        self.parent = parent
        self.client = client
        self.user_id = user_id
        self.tasks = []  # Список для хранения задач
        self.task_entry_frame = None  # Фрейм для ввода задачи
        self.task_texts = {}  # Словарь для хранения оригинальных текстов задач
        self.task_status = {}  # Словарь для хранения статусов

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
        self.button_tasks_frame.pack(fill="both", padx=5, pady=(10, 0))

        # Кнопки для работы с задачами
        self.add_task_button = ctk.CTkButton(self.button_tasks_frame, text="Добавить задачу",
                                             command=self.show_task_entry)
        self.add_task_button.grid(row=0, column=0, pady=10, padx=30)

        self.save_tasks_button = ctk.CTkButton(self.button_tasks_frame, text="Сохранить задачи",
                                               command=self.save_tasks_to_db)
        self.save_tasks_button.grid(row=0, column=1, pady=10, padx=30)

        self.error_label = ctk.CTkLabel(frame, text="")
        self.error_label.pack()

        self.get_tasks_from_server()

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

    def save_tasks_to_db(self):
        """Отправляет все задачи пользователя на сервер для сохранения в БД."""

        if self.client.connect():
            response = self.client.send_data(f"DELETE_TASKS_FROM_USER_ID;{self.user_id}")

            if response == "OK":
                print("[INFO] Задачи удалены")

        if not self.tasks:  # Проверяем, есть ли вообще задачи
            self.error_label.configure(text="Нет задач для сохранения!", text_color="red")
            return

        # Проверяем, совпадает ли количество задач и статусов
        if len(self.tasks) != len(self.task_status):
            self.error_label.configure(text="Ошибка: несоответствие задач и статусов!", text_color="red")
            print("[ERROR] Количество задач и статусов не совпадает!")
            return

        all_success = True  # Флаг успешного сохранения всех задач

        for task, task_status_var in zip(self.tasks, self.task_status.values()):
            task_text = task  # Текст задачи

            # Получаем сам текст статуса
            task_status_text = task_status_var.get() if isinstance(task_status_var, ctk.StringVar) else task_status_var

            if self.client.connect():
                print(f"[INFO] Отправка задачи: '{task_text}', статус: '{task_status_text}'")

                # Отправляем данные на сервер
                response = self.client.send_data(f"ADD_TASK;{self.user_id};{task_text};{task_status_text}")

                if response != "OK":
                    all_success = False

        # Проверяем, успешно ли сохранены все задачи
        if all_success:
            self.error_label.configure(text="Все задачи успешно сохранены!", text_color="green")
        else:
            self.error_label.configure(text="Ошибка при сохранении некоторых задач!", text_color="red")

    def get_tasks_from_server(self):
        """Запрашивает задачи с сервера и отображает их на экране"""
        if self.client.connect():
            # Отправляем команду на сервер для получения задач
            task_data = self.client.send_data(f"GET_TASKS;{self.user_id}")

            if task_data != "ERROR" and task_data != "NO_TASKS":
                tasks = task_data.split("\n")
                for task_info in tasks:
                    if task_info.strip():  # Проверяем, что строка не пустая
                        task_parts = task_info.split("|")
                        if len(task_parts) == 2:  # Проверяем, что строка разделена на 2 части
                            task_text, task_status = task_parts
                            self.add_task_to_ui(task_text, task_status)
                        else:
                            print(f"[ERROR] Неверный формат задачи: {task_info}")
            elif task_data == "NO_TASKS":
                print("[INFO] У пользователя нет задач.")
            else:
                print("[ERROR] Не удалось получить задачи.")

    def add_task_to_ui(self, task_text, task_status):
        """Добавляет задачу в пользовательский интерфейс"""
        task_frame = ctk.CTkFrame(self.tasks_frame)
        task_frame.pack(fill="x", pady=5)

        # Метка с текстом задачи
        task_label = ctk.CTkLabel(task_frame, text=task_text, anchor="w", font=("Arial", 14, "normal"))
        task_label.pack(side="left", padx=5, fill="x", expand=True)

        # 🔹 Сохраняем оригинальный текст в словаре
        self.task_texts[task_label] = task_text
        self.tasks.append(task_text)

        # Кнопка удаления
        delete_button = ctk.CTkButton(task_frame, text="❌", width=30,
                                      command=lambda: self.remove_task(task_frame, task_label, task_text))
        delete_button.pack(side="right", padx=5)

        # Кнопка редактирования
        edit_button = ctk.CTkButton(task_frame, text="✏", width=30,
                                    command=lambda: self.edit_task(task_label, task_frame, edit_button,
                                                                   status_dropdown))
        edit_button.pack(side="right", padx=5)

        # Выпадающий список для выбора состояния
        status_var = ctk.StringVar(value=task_status)
        self.update_task_status(task_label, status_var)
        status_options = ["Не выполнено", "В процессе", "Выполнено"]
        status_dropdown = ctk.CTkComboBox(task_frame, values=status_options, variable=status_var, state="readonly",
                                          command=lambda s: self.update_task_status(task_label, status_var))
        status_dropdown.pack(side="right", padx=5)

        # Добавляем состояние в словарь
        self.task_status[task_label] = status_var

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
            self.tasks.append(task_text)

            # Кнопка удаления
            delete_button = ctk.CTkButton(task_frame, text="❌", width=30,
                                          command=lambda: self.remove_task(task_frame, task_label, task_text))
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

            # Добавляем состояние в словарь
            self.task_status[task_label] = status_var

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

        # обновляем состояние в словаре
        self.task_status[task_label] = status_var
        # 🔹 Получаем оригинальный текст из словаря
        task_text = self.task_texts.get(task_label, task_label.cget("text"))

        # Обновляем текст с новым статусом
        if status == "Выполнено":
            task_label.configure(font=("Arial", 14, "normal"), text=task_text + " ✅", text_color="Green")
        elif status == "В процессе":
            task_label.configure(font=("Arial", 14, "normal"), text=task_text + " ⏳", text_color="Orange")
        elif status == "Не выполнено":
            task_label.configure(font=("Arial", 14, "normal"), text=task_text + " ❌", text_color="Red")

    def remove_task(self, task_frame, task_label, task_text):
        """Удаление задачи"""
        self.tasks.remove(task_text)
        self.task_texts.pop(task_label, None)  # 🔹 Удаляем текст из словаря
        self.task_status.pop(task_label)
        task_frame.destroy()
