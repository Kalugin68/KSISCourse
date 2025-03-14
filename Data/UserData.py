from Data import ConnectDatabase
from tkinter import messagebox


class UserDatabase(ConnectDatabase.Database):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.user = (self.username, self.password)

    def create_user_db(self):
        if self.connect_db():
            try:
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                        id SERIAL PRIMARY KEY,
                                        username VARCHAR(30) NOT NULL,
                                        password VARCHAR(20) NOT NULL)"""
                                    )
                print("[INFO] Таблица users создана или уже существует.")

                self.cursor.execute("""INSERT INTO users (username, password) VALUES
                (%s, %s)""", self.user)
                print("[INFO] Данные о пользователе добавлены")

            except Exception as ex:
                messagebox.showerror("Ошибка", f"Ошибка работы с PostgreSQL: {ex}")

            finally:
                self.close_connection()

    def check_user(self, username, password):
        """Проверяет, существует ли пользователь в базе данных."""
        if self.connect_db():
            try:
                self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                                    (username, password))
                user = self.cursor.fetchone()
                return user is not None  # Если запись найдена, возвращаем True

            except Exception as ex:
                messagebox.showerror("Ошибка", f"Ошибка при проверке пользователя: {ex}")
                return False

            finally:
                self.close_connection()