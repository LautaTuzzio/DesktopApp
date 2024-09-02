
import pygame
import random
import sys
import mysql.connector
from mysql.connector import Error
import datetime
import time

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
FPS = 20
user_id = sys.argv[1]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.start_time = time.time()

    def reset_game(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 + BLOCK_SIZE, HEIGHT // 2), (WIDTH // 2 + BLOCK_SIZE * 2, HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.apple = self.generate_apple()
        self.score = len(self.snake)

    def generate_apple(self):
        while True:
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            apple_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if not any(apple_rect.collidepoint(snake_pos) for snake_pos in self.snake):
                return (x, y)

    def update_snake(self):
        head = self.snake[-1]
        new_head = head

        if self.direction == 'UP':
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + BLOCK_SIZE)
        elif self.direction == 'LEFT':
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif self.direction == 'RIGHT':
            new_head = (head[0] + BLOCK_SIZE, head[1])

        self.snake.append(new_head)

        if self.snake[-1] == self.apple:
            self.apple = self.generate_apple()
            self.score += 1
        else:
            self.snake.pop(0)

    def draw_elements(self):
        self.screen.fill(BLACK)
        for pos in self.snake:
            pygame.draw.rect(self.screen, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, RED, (self.apple[0], self.apple[1], BLOCK_SIZE, BLOCK_SIZE))

        font = pygame.font.SysFont(None, 32)
        score_text = font.render(f"Score: {self.score-3}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def pause(self):
        DieFont = pygame.font.SysFont('Calibri', 40)
        restartFont = pygame.font.SysFont('Calibri', 20)

        text_die = DieFont.render("Game Over", True, (255, 255, 255))
        self.screen.blit(text_die, (325, 250))
            
        text_die_restart = restartFont.render("Space to restart", True, (255, 255, 255))
        self.screen.blit(text_die_restart, (345, 290))

        pygame.display.update()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart()
                        paused = False
                        return self.restart()

    def restart(self):
        fps = pygame.time.Clock()
        self.snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 + BLOCK_SIZE, HEIGHT // 2), (WIDTH // 2 + BLOCK_SIZE * 2, HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.apple = self.generate_apple()
        self.score = len(self.snake)
        return self.score - 3, fps

    def update_game_time(self, cursor, connection, user_id):
        current_time = time.time()
        elapsed_time = int(current_time - self.start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_format = f"{hours:02}:{minutes:02}:{seconds:02}"

        query_update_time = """UPDATE actividad SET tiempo = ADDTIME(tiempo, %s), ult_ingreso = %s WHERE id_user = %s AND id_juego = 1"""
        cursor.execute(query_update_time, (time_format, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        connection.commit()

    def scoreQuery(self):
        try:
            config = {
                "host": "localhost",
                "database": "desktopapp",
                "user": "root",
                "password": ""
            }
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                cursor = connection.cursor()

                query_check_user = "SELECT puntaje FROM actividad WHERE id_user = %s AND id_juego = 1"
                cursor.execute(query_check_user, (user_id,)) 
                result = cursor.fetchone()

                if result is not None:
                    db_score = result[0]
                    if db_score <= self.score:
                        query_update_max_score = "UPDATE actividad SET puntaje = %s WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_update_max_score, ((self.score-3), user_id))

                    if db_score > 0:
                        query_primer_logro = "UPDATE actividad SET logro = '001' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_primer_logro, (user_id,))

                    if db_score >= 20:
                        query_segundo_logro = "UPDATE actividad SET logro = '011' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_segundo_logro, (user_id,))

                    if db_score >= 1197:
                        query_tercer_logro = "UPDATE actividad SET logro = '111' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_tercer_logro, (user_id,))

                else:
                    query_insert_new_user = """INSERT INTO actividad (id_user, id_juego, puntaje, tiempo, ult_ingreso) VALUES (%s, 1, %s, 0, %s)"""
                    cursor.execute(query_insert_new_user, (user_id, self.score, datetime.datetime.now().strftime('%Y-%m-%d')))

                self.update_game_time(cursor, connection, user_id)

                query_update_last_login = """UPDATE actividad SET ult_ingreso = %s WHERE id_user = %s AND id_juego = 1"""
                cursor.execute(query_update_last_login, (datetime.datetime.now().strftime('%Y-%m-%d'), user_id))
                connection.commit()

        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def play(self):
        running = True
        paused = False
        while running:
            self.handle_events()
            if not paused:
                self.update_snake()
                
                if (self.snake[-1][0] < 0 or self.snake[-1][0] >= WIDTH or
                    self.snake[-1][1] < 0 or self.snake[-1][1] >= HEIGHT or
                    self.snake[-1] in self.snake[:-1]):
                    self.scoreQuery()
                    self.pause()
                    continue

            self.draw_elements()
            pygame.display.flip()
            self.clock.tick(FPS)

        if self.score == (WIDTH // BLOCK_SIZE * HEIGHT // BLOCK_SIZE):
            self.game_won_screen()

    def game_won_screen(self):
        self.screen.fill(WHITE)
        font = pygame.font.SysFont(None, 64)
        victory_text = font.render("¡Felicidades! Has ganado", True, BLACK)
        score_text = font.render(f"Tienes un score de {self.score} puntos", True, BLACK)
        play_again_text = font.render("Presiona Enter para jugar de nuevo", True, BLACK)
        
        self.screen.blit(victory_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        self.screen.blit(score_text, (WIDTH // 2 - 120, HEIGHT // 2 - 30))
        self.screen.blit(play_again_text, (WIDTH // 2 - 150, HEIGHT // 2 + 40))
        
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game = SnakeGame()
    game.play()
