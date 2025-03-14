from Data import ConnectDatabase
from tkinter import messagebox

class TasksDatabase(ConnectDatabase.Database):
    def __init__(self, task):
        super().__init__()
        self.task = task

    def create_tasks_db(self):
        if self.connect_db():
            try:
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                                        id SERIAL PRIMARY KEY,
                                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                                        task VARCHAR(200) NOT NULL)"""
                                    )
                print("[INFO] Таблица tasks создана или уже существует.")

            except Exception as ex:
                messagebox.showerror("Ошибка", f"Ошибка работы с PostgreSQL: {ex}")

            finally:
                self.close_connection()

    def add_task(self, user_id, task):
        if self.connect_db():
            try:
                self.cursor.execute("INSERT INTO tasks (user_id, task) VALUES (%s, %s);",
                                    (user_id, task))

                print(f"[INFO] Задача '{task}' добавлена для пользователя с id {user_id}.")

            except Exception as ex:
                print(f"[ERROR] Ошибка при добавлении задачи: {ex}")

            finally:
                self.close_connection()