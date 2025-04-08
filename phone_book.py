import psycopg2
import csv

conn_data = {
    "host": "localhost",
    "database": "lab10",
    "user": "postgres",
    "password": "aluak1122"
}

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with psycopg2.connect(**conn_data) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (name, phone))
    print("Добавлено!")

def insert_from_csv(path):
    with open(path, 'r', encoding="utf8") as f, psycopg2.connect(**conn_data) as conn:
        reader = csv.DictReader(f)
        with conn.cursor() as cur:
            for row in reader:
                cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                            (row['username'], row['phone']))
    print("CSV данные загружены!")

def update_user(old_name):
    new_name = input("New name (или Enter, чтобы пропустить): ")
    new_phone = input("New phone (или Enter, чтобы пропустить): ")
    with psycopg2.connect(**conn_data) as conn:
        with conn.cursor() as cur:
            if new_name:
                cur.execute("UPDATE phonebook SET username = %s WHERE username = %s", (new_name, old_name))
            if new_phone:
                cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_phone, old_name))
    print("Обновлено!")

def query_data(value):
    with psycopg2.connect(**conn_data) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s OR phone ILIKE %s",
                        (f'%{value}%', f'%{value}%'))
            results = cur.fetchall()
            for row in results:
                print(row)

def delete_user(value):
    with psycopg2.connect(**conn_data) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE username = %s OR phone = %s", (value, value))
    print("Удалено!")

if __name__ == "__main__":
    while True:
        print("\n=== Телефонный справочник ===")
        print("1. Добавить контакт вручную")
        print("2. Загрузить контакты из CSV")
        print("3. Обновить контакт")
        print("4. Найти контакт")
        print("5. Удалить контакт")
        print("0. Выход")

        выбор = input("Выберите действие: ")

        if выбор == "1":
            insert_from_console()
        elif выбор == "2":
            insert_from_csv("data/phone_book.csv")
        elif выбор == "3":
            старое_имя = input("Введите текущее имя контакта: ")
            update_user(старое_имя)
        elif выбор == "4":
            значение = input("Введите имя или номер для поиска: ")
            query_data(значение)
        elif выбор == "5":
            значение = input("Введите имя или номер для удаления: ")
            delete_user(значение)
        elif выбор == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
