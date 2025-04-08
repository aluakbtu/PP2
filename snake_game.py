import pygame
import psycopg2
import sys

conn_data = {
    "host": "localhost",
    "database": "lab10",
    "user": "postgres",
    "password": "aluak1122"
}

def get_user(username):
    with psycopg2.connect(**conn_data) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user:
                return user[0]
            cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
            return cur.fetchone()[0]

def get_user_level(user_id):
    with psycopg2.connect(**conn_data) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT level FROM user_score WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            return result[0] if result else 1

def save_game(user_id, level, score, game_state):
    with psycopg2.connect(**conn_data) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_score (user_id, level, score, game_state)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET level = EXCLUDED.level, score = EXCLUDED.score, game_state = EXCLUDED.game_state
            """, (user_id, level, score, game_state))

def play_game(username):
    user_id = get_user(username)
    level = get_user_level(user_id)
    print(f"Добро пожаловать, {username}! Ваш уровень: {level}")

    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption(f"Snake Game - Level {level}")
    clock = pygame.time.Clock()
    running = True
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(user_id, level, score, "quit")
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    save_game(user_id, level, score, "paused")
                    print("Игра сохранена (пауза).")

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(5 + level * 2)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    username = input("Введите ваше имя: ")
    play_game(username)

if __name__ == "__main__":
    print("=== Игра 'Змейка' ===")
    имя = input("Введите ваше имя пользователя: ")
    play_game(имя)
