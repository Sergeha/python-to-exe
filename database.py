# import sqlite3
#
# # Функция для создания соединения с базой данных
# def create_connection(db_file):
#     conn = sqlite3.connect(db_file)
#     return conn
#
# # Функция для закрытия соединения с базой данных
# def close_connection(conn):
#     if conn:
#         conn.close()
#
# # Функция для добавления записи
# def add_record(conn, registration_number, deceased_full_name, birth_date, burial_date, cemetery_name,
#                responsible_name, responsible_address_phone):
#     cursor = conn.cursor()
#
#     cursor.execute("""
#         INSERT INTO burial (registration_number, deceased_full_name, birth_date, burial_date, cemetery_name,
#                             responsible_name, responsible_address_phone)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, (registration_number, deceased_full_name, birth_date, burial_date, cemetery_name, responsible_name, responsible_address_phone))
#
#     conn.commit()
#
# # Функция для поиска записи по регистрационному номеру
# def search_by_registration_number(conn, registration_number):
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT * FROM burial WHERE registration_number = ?", (registration_number,))
#     records = cursor.fetchall()
#
#     return records
#
# # Функция для удаления записи
# def delete_record(conn, registration_number):
#     cursor = conn.cursor()
#
#     cursor.execute("DELETE FROM burial WHERE registration_number = ?", (registration_number,))
#
#     conn.commit()
#
#
# def search_by_full_name_or_last_name(conn, search_term):
#     cursor = conn.cursor()
#     query = '''
#     SELECT * FROM burial_records
#     WHERE deceased_full_name LIKE ? OR deceased_full_name LIKE ?
#     '''
#     search_pattern = f"%{search_term}%"
#     cursor.execute(query, (search_pattern, search_pattern))
#     return cursor.fetchall()
#
#
# # Функция для создания таблицы, если она не существует
# def create_table(conn):
#     cursor = conn.cursor()
#
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS burial (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             registration_number TEXT NOT NULL,
#             deceased_full_name TEXT NOT NULL,
#             birth_date TEXT NOT NULL,
#             burial_date TEXT NOT NULL,
#             cemetery_name TEXT NOT NULL,
#             responsible_name TEXT NOT NULL,
#             responsible_address_phone TEXT NOT NULL
#         );
#     """)
#
#     conn.commit()
import sqlite3

# Функция для создания соединения с базой данных
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

# Функция для закрытия соединения с базой данных
def close_connection(conn):
    if conn:
        conn.close()

# Функция для добавления записи
def add_record(conn, registration_number, deceased_full_name, birth_date, burial_date, cemetery_name,
               responsible_name, responsible_address_phone):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO burial (registration_number, deceased_full_name, birth_date, burial_date, cemetery_name, 
                            responsible_name, responsible_address_phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (registration_number, deceased_full_name, birth_date, burial_date, cemetery_name, responsible_name, responsible_address_phone))

    conn.commit()

# Функция для поиска записи по регистрационному номеру
def search_by_registration_number(conn, registration_number):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM burial WHERE registration_number = ?", (registration_number,))
    records = cursor.fetchall()

    return records

# Функция для удаления записи
def delete_record(conn, registration_number):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM burial WHERE registration_number = ?", (registration_number,))

    conn.commit()

# Функция для поиска записи по фамилии или ФИО
def search_by_full_name_or_last_name(conn, search_term):
    cursor = conn.cursor()
    query = '''
    SELECT * FROM burial
    WHERE deceased_full_name LIKE ? OR deceased_full_name LIKE ?
    '''
    search_pattern = f"%{search_term}%"
    cursor.execute(query, (search_pattern, search_pattern))
    return cursor.fetchall()

# Функция для создания таблицы, если она не существует
def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS burial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT NOT NULL,
            deceased_full_name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            burial_date TEXT NOT NULL,
            cemetery_name TEXT NOT NULL,
            responsible_name TEXT NOT NULL,
            responsible_address_phone TEXT NOT NULL
        );
    """)

    conn.commit()

