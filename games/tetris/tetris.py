import pygame
import random
import sys
import time
import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta
import os

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
SIDEBAR_COLOR = (158,173,134,255)  
TEXT_COLOR = (1,0,0,255)

BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 6
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + SIDEBAR_WIDTH)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
user_id = sys.argv[1]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.game_over = False
        self.score = 0
        self.start_time = time.time()
        self.font = pygame.font.Font(None, 36)
        
      
        self.grid_sprite = pygame.image.load(os.path.join('games', 'tetris', 'bg.jpg'))
        self.grid_sprite = pygame.transform.scale(self.grid_sprite, (BLOCK_SIZE, BLOCK_SIZE))

        self.tetromino_sprite = pygame.image.load(os.path.join('games', 'tetris', 'piece.jpg'))
        self.tetromino_sprite = pygame.transform.scale(self.tetromino_sprite, (BLOCK_SIZE, BLOCK_SIZE))

        self.down_arrow_img = pygame.image.load(os.path.join('games', 'tetris', 'arrow-down.png'))
        self.down_arrow_img = pygame.transform.scale(self.down_arrow_img, (BLOCK_SIZE, BLOCK_SIZE))

        self.up_arrow_img = pygame.image.load(os.path.join('games', 'tetris', 'arrow-up.png'))
        self.up_arrow_img = pygame.transform.scale(self.up_arrow_img, (BLOCK_SIZE, BLOCK_SIZE))

        self.right_arrow_img = pygame.image.load(os.path.join('games', 'tetris', 'arrow-right.png'))
        self.right_arrow_img = pygame.transform.scale(self.right_arrow_img, (BLOCK_SIZE, BLOCK_SIZE))

        self.left_arrow_img = pygame.image.load(os.path.join('games', 'tetris', 'arrow-left.png'))
        self.left_arrow_img = pygame.transform.scale(self.left_arrow_img, (BLOCK_SIZE, BLOCK_SIZE))
        
        self.db_connection = None
        self.connect_to_database()
        self.last_death_time = time.time()

    def connect_to_database(self):
            try:
                self.db_connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='desktopapp'
                )
                if self.db_connection.is_connected():
                    print("Successfully connected to the database")
            except Error as e:
                print(f"Error connecting to database: {e}")
                sys.exit()

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.screen.blit(self.grid_sprite, (x * BLOCK_SIZE, y * BLOCK_SIZE))  
                if self.grid[y][x] != BLACK:
                    self.screen.blit(self.tetromino_sprite, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    def draw_current_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.screen.blit(self.tetromino_sprite, 
                                    ((self.current_piece.x + x) * BLOCK_SIZE,
                                    (self.current_piece.y + y) * BLOCK_SIZE))

    def draw_next_piece(self):
        start_x = GRID_WIDTH + 1
        start_y = 4
        
        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.screen.blit(self.tetromino_sprite, 
                                    ((start_x + x) * BLOCK_SIZE,
                                    (start_y + y) * BLOCK_SIZE))
    def draw_sidebar(self):
        pygame.draw.rect(self.screen, SIDEBAR_COLOR, 
                        (GRID_WIDTH * BLOCK_SIZE, 0, SIDEBAR_WIDTH * BLOCK_SIZE, SCREEN_HEIGHT))

        title_text = self.font.render("TETRIS", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(GRID_WIDTH * BLOCK_SIZE + SIDEBAR_WIDTH * BLOCK_SIZE / 2, BLOCK_SIZE * 2))
        self.screen.blit(title_text, title_rect)

        padding = 20

        next_text = self.font.render("Siguiente:", True, TEXT_COLOR)
        self.screen.blit(next_text, (GRID_WIDTH * BLOCK_SIZE + 10, 4 * BLOCK_SIZE + padding))

        start_x = GRID_WIDTH + 1
        start_y = 6 + padding // BLOCK_SIZE 

        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.screen.blit(self.tetromino_sprite, 
                                    ((start_x + x) * BLOCK_SIZE,
                                    (start_y + y) * BLOCK_SIZE))

        score_text = self.font.render(f"Puntos: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 8 * BLOCK_SIZE + 2 * padding))

        elapsed_time = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        time_text = self.font.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, TEXT_COLOR)
        self.screen.blit(time_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10 * BLOCK_SIZE + 3 * padding))

        padding_x = 10  
        padding_y = 10 
        base_y = SCREEN_HEIGHT - 150

        self.screen.blit(self.down_arrow_img, (GRID_WIDTH * BLOCK_SIZE + padding_x, base_y))
        self.screen.blit(self.font.render("Abajo", True, TEXT_COLOR), (GRID_WIDTH * BLOCK_SIZE + 2 * padding_x + BLOCK_SIZE, base_y))

        self.screen.blit(self.up_arrow_img, (GRID_WIDTH * BLOCK_SIZE + padding_x, base_y + BLOCK_SIZE + padding_y))
        self.screen.blit(self.font.render("Rotar", True, TEXT_COLOR), (GRID_WIDTH * BLOCK_SIZE + 2 * padding_x + BLOCK_SIZE, base_y + BLOCK_SIZE + padding_y))

        self.screen.blit(self.right_arrow_img, (GRID_WIDTH * BLOCK_SIZE + padding_x, base_y + 2 * (BLOCK_SIZE + padding_y)))
        self.screen.blit(self.font.render("Derecha", True, TEXT_COLOR), (GRID_WIDTH * BLOCK_SIZE + 2 * padding_x + BLOCK_SIZE, base_y + 2 * (BLOCK_SIZE + padding_y)))

        self.screen.blit(self.left_arrow_img, (GRID_WIDTH * BLOCK_SIZE + padding_x, base_y + 3 * (BLOCK_SIZE + padding_y)))
        self.screen.blit(self.font.render("Izquierda", True, TEXT_COLOR), (GRID_WIDTH * BLOCK_SIZE + 2 * padding_x + BLOCK_SIZE, base_y + 3 * (BLOCK_SIZE + padding_y)))

    def show_game_over_message(self):
        self.screen.fill(BLACK)

        game_over_text = self.font.render("¡Perdiste!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(game_over_text, text_rect)

        score_text = self.font.render(f"Puntos: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(score_text, score_rect)

        play_again_text = self.font.render("Jugar de nuevo", True, WHITE)
        play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(play_again_text, play_again_rect)

        quit_text = self.font.render("Salir", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        self.execute_game_over_queries()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_again_rect.collidepoint(mouse_pos):
                        return True  
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    def reset_game(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.start_time = time.time()
        self.last_death_time = time.time()


    def move(self, dx, dy):
        if self.valid_move(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def valid_move(self, piece, dx, dy):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = piece.x + x + dx, piece.y + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return False
        return True


    def rotate_piece(self):
        original_shape = self.current_piece.shape
        original_x = self.current_piece.x
        rotated = list(zip(*self.current_piece.shape[::-1]))
        self.current_piece.shape = rotated

        while not self.valid_move(self.current_piece, 0, 0):
            self.current_piece.x -= 1
            if self.current_piece.x < 0:
                self.current_piece.shape = original_shape
                self.current_piece.x = original_x
                break

    def place_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_piece.y + y
                    grid_x = self.current_piece.x + x
                    if 0 <= grid_y < GRID_HEIGHT and 0 <= grid_x < GRID_WIDTH:
                        self.grid[grid_y][grid_x] = self.current_piece.color
                    else:
                        print(f"Warning: Attempted to place piece outside grid bounds at ({grid_x}, {grid_y})")
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        if not self.valid_move(self.current_piece, 0, 0):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        new_grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(lines_cleared)] + new_grid
        self.grid = new_grid
        self.score += lines_cleared ** 2 * 100
        
    def run(self):
        while True:  
            self.reset_game() 
            fall_time = 0
            fall_speed = 0.5
            self.game_over = False
            down_press_time = 0
            down_delay = 100  

            while not self.game_over:
                fall_time += self.clock.get_rawtime()
                current_time = pygame.time.get_ticks()
                self.clock.tick()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_w or event.key == pygame.K_UP:
                            self.rotate_piece()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    if current_time - down_press_time > down_delay:
                        self.move(0, 1)
                        down_press_time = current_time
                else:
                    down_press_time = current_time - down_delay 

                if fall_time / 1000 > fall_speed:
                    if not self.move(0, 1):
                        self.place_piece()
                    fall_time = 0

                self.screen.fill(BLACK)
                self.draw_grid()
                self.draw_current_piece()
                self.draw_sidebar()
                pygame.display.flip()

            self.elapsed_time = int(time.time() - self.start_time)

            if not self.show_game_over_message():
                break

    def execute_game_over_queries(self):
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()

                check_record_query = """
                SELECT COUNT(*) FROM actividad 
                WHERE id_user = %s AND id_juego = %s
                """
                cursor.execute(check_record_query, (user_id, 3))
                record_exists = cursor.fetchone()[0] > 0
                print(record_exists)

                if not record_exists:
                    insert_new_record_query = """
                    INSERT INTO actividad (id_user, id_juego, logro, estilos, tiempo, ult_ingreso, puntaje)
                    VALUES (%s, %s, 0, 000, '00:00:00', %s, 0)
                    """
                    cursor.execute(insert_new_record_query, (user_id, 3, date.today()))

                update_time_query = """
                UPDATE actividad 
                SET tiempo = ADDTIME(tiempo, SEC_TO_TIME(%s)) 
                WHERE id_user = %s AND id_juego = %s
                """
                cursor.execute(update_time_query, (self.elapsed_time, user_id, 3))

                update_date_query = """
                UPDATE actividad 
                SET ult_ingreso = %s 
                WHERE id_user = %s AND id_juego = %s
                """
                cursor.execute(update_date_query, (date.today(), user_id, 3))

                update_score_query = """
                UPDATE actividad 
                SET puntaje = GREATEST(puntaje, %s)
                WHERE id_user = %s AND id_juego = %s
                """
                cursor.execute(update_score_query, (self.score, user_id, 3))

                achievement_bitmask = 0
                coin_reward = 0

                if self.score >= 1000:
                    achievement_bitmask += 1
                    coin_reward += 1000  

                if self.score >= 10000:
                    achievement_bitmask += 10
                    coin_reward += 3000 

                if self.score >= 100000:
                    achievement_bitmask += 100
                    coin_reward += 10000  

                print(f"Achievement bitmask: {achievement_bitmask}, Coin reward: {coin_reward}")

                if achievement_bitmask > 0:
                    update_achievements_query = """
                    UPDATE actividad 
                    SET logro = logro + %s
                    WHERE id_user = %s AND id_juego = %s AND (logro & %s) = 0
                    """
                    cursor.execute(update_achievements_query, (achievement_bitmask, user_id, 3, achievement_bitmask))

                    update_coins_query = """
                    UPDATE usuario 
                    SET monedas = monedas + %s 
                    WHERE id_user = %s
                    """
                    cursor.execute(update_coins_query, (coin_reward, user_id))

                self.db_connection.commit()

                print("Game over queries executed successfully.")
            except mysql.connector.Error as err:
                print(f"Error executing game over queries: {err}")
            finally:
                cursor.close()
        else:
            print("No DB connection found")


game = TetrisGame()
game.run()

