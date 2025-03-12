import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tempfile
import os
from database import add_record, search_by_full_name_or_last_name, delete_record, create_table, create_connection, close_connection


class BurialRecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("База данных захоронений")
        self.root.geometry("700x700")

        self.conn = create_connection("database.db")
        create_table(self.conn)
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.add_frame = tk.Frame(self.notebook)
        self.search_frame = tk.Frame(self.notebook)
        self.delete_frame = tk.Frame(self.notebook)

        self.notebook.add(self.add_frame, text="Добавить запись")
        self.notebook.add(self.search_frame, text="Поиск записи")
        self.notebook.add(self.delete_frame, text="Удалить запись")

        self.create_add_tab()
        self.create_search_tab()
        self.create_delete_tab()

    def create_add_tab(self):
        fields = [
            ("Регистрационный номер:", "reg_number"),
            ("ФИО умершего:", "full_name"),
            ("Дата рождения (ГГГГ-ММ-ДД):", "birth_date"),
            ("Дата захоронения (ГГГГ-ММ-ДД):", "burial_date"),
            ("Название кладбища:", "cemetery"),
            ("ФИО ответственного:", "responsible"),
            ("Адрес и телефон ответственного:", "contact")
        ]

        self.entries = {}
        for label_text, key in fields:
            tk.Label(self.add_frame, text=label_text, font=("Arial", 18)).pack(pady=5)
            entry = tk.Entry(self.add_frame, font=("Arial", 18), width=40)
            entry.pack(pady=5)
            self.entries[key] = entry

        tk.Button(self.add_frame, text="Добавить", command=self.add_record_to_db, font=("Arial", 18)).pack(pady=20)

    def create_search_tab(self):
        self.search_label = tk.Label(self.search_frame, text="Введите фамилию или ФИО:", font=("Arial", 18))
        self.search_label.pack(pady=10)
        self.search_entry = tk.Entry(self.search_frame, font=("Arial", 18), width=40)
        self.search_entry.pack(pady=10)
        self.search_button = tk.Button(self.search_frame, text="Поиск", command=self.search_record_in_db, font=("Arial", 18))
        self.search_button.pack(pady=20)

    def create_delete_tab(self):
        self.delete_label = tk.Label(self.delete_frame, text="Введите рег. номер для удаления:", font=("Arial", 18))
        self.delete_label.pack(pady=10)
        self.delete_entry = tk.Entry(self.delete_frame, font=("Arial", 18), width=40)
        self.delete_entry.pack(pady=10)
        self.delete_button = tk.Button(self.delete_frame, text="Удалить", command=self.delete_record_from_db, font=("Arial", 18))
        self.delete_button.pack(pady=20)

    def add_record_to_db(self):
        values = [entry.get() for entry in self.entries.values()]
        add_record(self.conn, *values)
        messagebox.showinfo("Успех", "Запись добавлена!")
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def search_record_in_db(self):
        search_term = self.search_entry.get()
        records = search_by_full_name_or_last_name(self.conn, search_term)

        result_window = tk.Toplevel(self.root)
        result_window.title("Результаты поиска")
        result_window.geometry("700x700")

        canvas = tk.Canvas(result_window)
        canvas.pack(fill="both", expand=True)
        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        for record in records:
            record_text = f"Рег. номер: {record[1]}\nФИО: {record[2]}\nДата рождения: {record[3]}\nДата захоронения: {record[4]}\nКладбище: {record[5]}\nОтветственный: {record[6]}\nАдрес и телефон: {record[7]}"
            tk.Label(content_frame, text=record_text, font=("Arial", 18)).pack(pady=10)

        print_button = tk.Button(result_window, text="Распечатать", command=lambda: self.print_results(records), font=("Arial", 18))
        print_button.pack(pady=20)

        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def print_results(self, records):
        if not records:
            messagebox.showwarning("Печать", "Нет данных для печати.")
            return

        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".txt") as temp_file:
            for record in records:
                temp_file.write(
                    f"Рег. номер: {record[1]}\nФИО: {record[2]}\nДата рождения: {record[3]}\n"
                    f"Дата захоронения: {record[4]}\nКладбище: {record[5]}\n"
                    f"Ответственный: {record[6]}\nАдрес и телефон: {record[7]}\n\n"
                )
            temp_path = temp_file.name

        os.startfile(temp_path, "print")

    def delete_record_from_db(self):
        reg_number = self.delete_entry.get()
        confirm = messagebox.askyesno("Подтверждение", f"Удалить запись {reg_number}?")
        if confirm:
            delete_record(self.conn, reg_number)
            messagebox.showinfo("Успех", "Запись удалена!")

    def quit(self):
        close_connection(self.conn)
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = BurialRecordApp(root)
    root.mainloop()
