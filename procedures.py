import psycopg2

conn_data = {
    "host": "localhost",
    "database": "lab10",
    "user": "postgres",
    "password": "aluak1122"
}
#создание функций
def create_all():
    conn = psycopg2.connect(**conn_data)
    cur = conn.cursor()
    cur.execute("DROP FUNCTION IF EXISTS f_search(TEXT);")

    #1.поиск
    cur.execute("""
    CREATE OR REPLACE FUNCTION f_search(p TEXT)
    RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR)
    LANGUAGE plpgsql AS $$
    BEGIN
        RETURN QUERY
        SELECT pb.id, pb.username, pb.phone
        FROM phonebook pb
        WHERE pb.username ILIKE '%' || p || '%' OR pb.phone ILIKE '%' || p || '%';
    END;
    $$;
    """)

    #2.вставка/обновление
    cur.execute("""
    CREATE OR REPLACE PROCEDURE p_upsert(n TEXT, ph TEXT)
    LANGUAGE plpgsql AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM phonebook WHERE username = n) THEN
            UPDATE phonebook SET phone = ph WHERE username = n;
        ELSE
            INSERT INTO phonebook (username, phone) VALUES (n, ph);
        END IF;
    END;
    $$;
    """)

    #3.массовая вставка
    cur.execute("""
    CREATE OR REPLACE PROCEDURE p_insert_many(ns TEXT[], phs TEXT[], OUT bad TEXT[])
    LANGUAGE plpgsql AS $$
    DECLARE
        i INT;
        n TEXT;
        ph TEXT;
        wrong TEXT[] := '{}';
    BEGIN
        FOR i IN 1..array_length(ns, 1) LOOP
            n := ns[i];
            ph := phs[i];
            IF ph ~ '^87[0-9]{9}$' THEN
                CALL p_upsert(n, ph);
            ELSE
                wrong := array_append(wrong, n || ' - ' || ph);
            END IF;
        END LOOP;
        bad := wrong;
    END;
    $$;
    """)

    #4.пагинация
    cur.execute("""
    CREATE OR REPLACE FUNCTION f_page(lim INT, off INT)
    RETURNS TABLE(id INT, name TEXT, phone TEXT)
    LANGUAGE plpgsql AS $$
    BEGIN
        RETURN QUERY
        SELECT id, username, phone FROM phonebook ORDER BY id LIMIT lim OFFSET off;
    END;
    $$;
    """)

    #5.удаление
    cur.execute("""
    CREATE OR REPLACE PROCEDURE p_del(val TEXT)
    LANGUAGE plpgsql AS $$
    BEGIN
        DELETE FROM phonebook WHERE username = val OR phone = val;
    END;
    $$;
    """)

    conn.commit()
    cur.close()
    conn.close()

def run_console():
    conn = psycopg2.connect(**conn_data)
    cur = conn.cursor()

    while True:
        print("1.найти по имени/номеру")
        print("2.добавить/обновить контакт")
        print("3.массовая вставка")
        print("4.пагинация")
        print("5.удалить по имени/номеру")
        print("0.выход")

        choice = input("действие: ")

        if choice == "1":
            p = input("введите часть имени/номера: ")
            cur.execute("SELECT * FROM f_search(%s)", (p,))
            for row in cur.fetchall():
                print(row)

        elif choice == "2":
            name = input("имя: ")
            phone = input("телефон: ")
            cur.execute("CALL p_upsert(%s, %s)", (name, phone))
            print("контакт сохранён")

        elif choice == "3":
            names = input("введите имена через запятую: ").split(',')
            phones = input("введите телефоны через запятую: ").split(',')
            cur.execute("CALL p_insert_many(%s, %s, %s)", (names, phones, None))
            print("массовая вставка выполнена")

        elif choice == "4":
            lim = int(input("сколько показать записей: "))
            off = int(input("с какого начать: "))
            cur.execute("SELECT * FROM f_page(%s, %s)", (lim, off))
            for row in cur.fetchall():
                print(row)

        elif choice == "5":
            val = input("введите имя/номер для удаления: ")
            cur.execute("CALL p_del(%s)", (val,))
            print("удалено")

        elif choice == "0":
            break
        else:
            print("попробуйте снова")

    conn.commit()
    cur.close()
    conn.close()

create_all()
run_console()
