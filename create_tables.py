import psycopg2

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_score (
            user_id INTEGER PRIMARY KEY REFERENCES users(id),
            level INTEGER NOT NULL,
            score INTEGER NOT NULL,
            game_state TEXT
        )
        """
    ]
    conn = psycopg2.connect(
        host="localhost",
        database="lab10",
        user="postgres",
        password="aluak1122"
    )
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы успешно созданы.")

if __name__ == '__main__':
    create_tables()
