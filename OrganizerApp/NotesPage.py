import customtkinter as ctk
from CTkListbox import *
import uuid  # Для генерации уникальных ID


class NotePage:
    def __init__(self, parent_frame, client, user_id):
        """Создаем менеджер заметок внутри переданного родительского виджета"""
        self.parent_frame = parent_frame
        self.client = client
        self.user_id = user_id
        self.notes = {}  # {note_id: text}
        self.note_ids = []  # Список ID для корректного удаления

    def create_notes_page(self):
        frame = ctk.CTkFrame(self.parent_frame)
        frame.pack(fill="both", expand=True)

        # Список заметок (слева)
        self.notes_listbox = CTkListbox(frame, width=200, height=300)
        self.notes_listbox.pack(side="left", padx=10, pady=(10, 100), fill="y")
        self.notes_listbox.bind("<<ListboxSelect>>", self.load_note)

        # Поля для заголовка и текста заметки
        self.title_entry = ctk.CTkEntry(frame, width=300, placeholder_text="Введите заголовок")
        self.title_entry.pack(side="top", padx=10, pady=5, fill="x")

        self.textbox = ctk.CTkTextbox(frame, width=300, height=100)
        self.textbox.pack(side="top", padx=10, pady=5, fill="x")

        # Кнопки
        self.add_button = ctk.CTkButton(frame, text="➕ Добавить", command=self.add_note)
        self.add_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(frame, text="🗑 Удалить", fg_color="red", command=self.delete_note)
        self.delete_button.pack(pady=5)

        self.save_button = ctk.CTkButton(frame, text="Сохранить изменения", command=self.save_note)
        self.save_button.pack(pady=5)

        self.get_notes_from_server()

        return frame

    def get_notes_from_server(self):
        """Запрашивает заметки с сервера и добавляет их в интерфейс"""
        if self.client.connect():
            note_data = self.client.send_data(f"GET_NOTES;{self.user_id}")

            if note_data and note_data not in ["ERROR", "NO_NOTES"]:
                notes = note_data.split("\n")

                self.notes.clear()
                self.note_ids.clear()
                self.notes_listbox.delete(0, "end")

                for note_info in notes:
                    if note_info.strip():
                        note_parts = note_info.split("|")
                        if len(note_parts) == 3:  # "note_id|title|text"
                            note_id, note_title, note_text = note_parts
                            self.notes[note_id] = (note_title, note_text)
                            self.note_ids.append(note_id)
                            self.notes_listbox.insert("end", note_title)

                print(f"[INFO] Загружено {len(self.notes)} заметок.")
            else:
                print("[INFO] У пользователя нет заметок или произошла ошибка.")

    def add_note(self):
        """Добавляет новую заметку"""
        if self.client.connect():
            title = self.title_entry.get().strip()
            text = self.textbox.get("1.0", "end").strip()

            if title and text:
                note_id = str(uuid.uuid4())  # Уникальный ID

                response = self.client.send_data(f"ADD_NOTE;{self.user_id};{note_id};{title};{text}")

                if response == "SUCCESS":
                    self.notes[note_id] = (title, text)
                    self.note_ids.append(note_id)
                    self.notes_listbox.insert("end", title)
                    self.title_entry.delete(0, "end")
                    self.textbox.delete("1.0", "end")
                else:
                    print("[ERROR] Не удалось добавить заметку")

    def load_note(self, event=None):
        """Загружает выбранную заметку"""
        selected_index = self.notes_listbox.curselection()

        if selected_index is not None:
            note_id = self.note_ids[selected_index]
            title, text = self.notes[note_id]
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, title)
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", text)

    def delete_note(self):
        """Удаляет заметку из UI и с сервера"""
        if self.client.connect():
            selected_index = self.notes_listbox.curselection()

            if selected_index is not None:
                note_id = self.note_ids.pop(selected_index)

                response = self.client.send_data(f"DELETE_NOTE;{note_id}")

                if response == "SUCCESS":
                    del self.notes[note_id]
                    self.notes_listbox.delete(selected_index)
                    self.textbox.delete("1.0", "end")
                    self.title_entry.delete(0, "end")
                else:
                    print("[ERROR] Ошибка удаления заметки")

    def save_note(self):
        """Обновляет текст и заголовок заметки"""
        if self.client.connect():
            selected_index = self.notes_listbox.curselection()

            if selected_index is not None:
                note_id = self.note_ids[selected_index]
                new_title = self.title_entry.get().strip()
                new_text = self.textbox.get("1.0", "end").strip()

                if new_title and new_text:
                    response = self.client.send_data(f"UPDATE_NOTE;{note_id};{new_title};{new_text}")
                    if response == "SUCCESS":
                        self.notes[note_id] = (new_title, new_text)
                        self.update_notes_list()
                    else:
                        print("[ERROR] Ошибка обновления заметки")

    def update_notes_list(self):
        """Обновляет список заметок"""
        self.notes_listbox.delete(0, 'end')

        for note_id, (title, _) in self.notes.items():
            self.notes_listbox.insert('end', title)
