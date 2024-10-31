import pygame
import sys
import random
import mysql.connector
import datetime

class Paddle:
    WIDTH, HEIGHT = 20, 100
    SPEED = 7

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def move(self, up=False):
        if up and self.rect.top > 0:
            self.rect.y -= self.SPEED
        elif not up and self.rect.bottom < Game.HEIGHT:
            self.rect.y += self.SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, Game.WHITE, self.rect)

class Ball:
    RADIUS = 10
    INITIAL_SPEED_X = 5
    INITIAL_SPEED_Y = 5
    SPEED_INCREASE = 0.7

    def __init__(self):
        self.rect = pygame.Rect(Game.WIDTH // 2 - self.RADIUS, Game.HEIGHT // 2 - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2)
        self.speed_x = self.INITIAL_SPEED_X * random.choice((1, -1))
        self.speed_y = self.INITIAL_SPEED_Y * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce(self, axis):
        if axis == 'x':
            self.speed_x *= -1
        elif axis == 'y':
            self.speed_y *= -1

        if self.speed_x > 0:
            self.speed_x += self.SPEED_INCREASE
        else:
            self.speed_x -= self.SPEED_INCREASE
        if self.speed_y > 0:
            self.speed_y += self.SPEED_INCREASE
        else:
            self.speed_y -= self.SPEED_INCREASE

    def reset(self):
        self.rect.center = (Game.WIDTH // 2, Game.HEIGHT // 2)
        self.speed_x = self.INITIAL_SPEED_X * random.choice((1, -1))
        self.speed_y = self.INITIAL_SPEED_Y * random.choice((1, -1))

    def draw(self, screen):
        pygame.draw.ellipse(screen, Game.WHITE, self.rect)

class Game:
    WIDTH, HEIGHT = 800, 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FPS = 60
    WINNING_SCORE = 7
    WINNING_DIFFERENCE = 2

    def __init__(self, user_id):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.menu_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.left_paddle = Paddle(10, self.HEIGHT // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(self.WIDTH - 30, self.HEIGHT // 2 - Paddle.HEIGHT // 2)
        self.ball = Ball()
        
        self.left_score = 0
        self.right_score = 0
        self.game_state = 'MENU'
        self.game_mode = 'PLAYER_VS_PLAYER'
        self.ai_paddle_speed = Paddle.SPEED
        self.user_id = user_id
        self.game_start_time = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == 'MENU':
                    if event.key == pygame.K_1:
                        self.game_mode = 'PLAYER_VS_PLAYER'
                        self.game_state = 'START_SCREEN'
                    elif event.key == pygame.K_2:
                        self.game_mode = 'PLAYER_VS_AI'
                        self.game_state = 'START_SCREEN'
                elif self.game_state == 'START_SCREEN':
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                elif self.game_state == 'GAME_OVER':
                    if event.key == pygame.K_SPACE:
                        self.game_state = 'MENU'
        return True


    def move_paddles(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move(up=True)
        if keys[pygame.K_s]:
            self.left_paddle.move(up=False)
        
        if self.game_mode == 'PLAYER_VS_PLAYER':
            if keys[pygame.K_UP]:
                self.right_paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                self.right_paddle.move(up=False)
        else:
            # AI movement
            if self.right_paddle.rect.centery < self.ball.rect.centery and self.right_paddle.rect.bottom < self.HEIGHT:
                self.right_paddle.rect.y += self.ai_paddle_speed
            elif self.right_paddle.rect.centery > self.ball.rect.centery and self.right_paddle.rect.top > 0:
                self.right_paddle.rect.y -= self.ai_paddle_speed

    def move_ball(self):
        self.ball.move()

        # Collision with top or bottom
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.HEIGHT:
            self.ball.bounce('y')

        # Collision with paddles
        if self.ball.rect.colliderect(self.left_paddle.rect) or self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.bounce('x')
            if self.game_mode == 'PLAYER_VS_AI':
                self.ai_paddle_speed += 0.1

        # Scoring
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.ball.reset()
        if self.ball.rect.right >= self.WIDTH:
            self.left_score += 1
            self.ball.reset()

    def check_winner(self):
        if (self.left_score >= self.WINNING_SCORE or self.right_score >= self.WINNING_SCORE) and \
           abs(self.left_score - self.right_score) >= self.WINNING_DIFFERENCE:
            return True
        return False

    def draw_game(self):
        self.screen.fill(self.BLACK)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        pygame.draw.aaline(self.screen, self.WHITE, (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT))

        left_text = self.font.render(str(self.left_score), True, self.WHITE)
        self.screen.blit(left_text, (self.WIDTH // 4, 20))

        right_text = self.font.render(str(self.right_score), True, self.WHITE)
        self.screen.blit(right_text, (self.WIDTH * 3 // 4, 20))

        pygame.display.flip()

    def draw_menu(self):
        self.screen.fill(self.BLACK)
        
        # Título principal
        title = self.font.render("PONG", True, self.WHITE)
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 100))
        
        instruction_font = pygame.font.Font(None, 24)  
        gray_color = (200, 200, 200)
        
        instruction1 = instruction_font.render("Presiona 1 o 2 para seleccionar una opcion", True, gray_color)
        self.screen.blit(instruction1, (self.WIDTH // 2 - instruction1.get_width() // 2, 180))

        # Opciones de menú
        pvp = self.menu_font.render("1. Jugador vs Jugador", True, self.WHITE)
        self.screen.blit(pvp, (self.WIDTH // 2 - pvp.get_width() // 2, 300))

        pva = self.menu_font.render("2. Jugador vs IA", True, self.WHITE)
        self.screen.blit(pva, (self.WIDTH // 2 - pva.get_width() // 2, 350))

        pygame.display.flip()


    def draw_game_over(self):
        self.screen.fill(self.BLACK)
        winner_text = "Jugador Izquierdo Gana!" if self.left_score > self.right_score else "Jugador Derecho Gana!"
        winner_surface = self.font.render(winner_text, True, self.WHITE)
        self.screen.blit(winner_surface, (self.WIDTH // 2 - winner_surface.get_width() // 2, self.HEIGHT // 2 - winner_surface.get_height() // 2))
        play_again = self.menu_font.render("Presiona espacio para jugar de nuevo", True, self.WHITE)
        self.screen.blit(play_again, (self.WIDTH // 2 - play_again.get_width() // 2, self.HEIGHT // 2 + 100))

        pygame.display.flip()

    def reset_game(self):
        self.left_score = 0
        self.right_score = 0
        self.ai_paddle_speed = Paddle.SPEED
        self.ball.reset()
        self.left_paddle.rect.centery = self.HEIGHT // 2
        self.right_paddle.rect.centery = self.HEIGHT // 2
        self.game_state = 'PLAYING'
        self.game_start_time = pygame.time.get_ticks()

    def db_config(self, winner):
        if self.game_mode != 'PLAYER_VS_AI' or winner != "Left Player":
            return

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

                query_check_user = "SELECT puntaje FROM actividad WHERE id_user = %s AND id_juego = 2"
                cursor.execute(query_check_user, (self.user_id,))
                result = cursor.fetchone()

                if result is not None:
                    current_victories = result[0]
                    new_victories = current_victories + 1
                    print(new_victories)
                    
                    query_update_victories = "UPDATE actividad SET puntaje = %s WHERE id_user = %s AND id_juego = 2"
                    cursor.execute(query_update_victories, (new_victories, self.user_id))

                    if new_victories == 5:
                        query_segundo_logro = "UPDATE actividad SET logro = '011' WHERE id_user = %s AND id_juego = 2"
                        cursor.execute(query_segundo_logro, (self.user_id,))
                    elif new_victories == 20:
                        query_tercer_logro = "UPDATE actividad SET logro = '111' WHERE id_user = %s AND id_juego = 2"
                        cursor.execute(query_tercer_logro, (self.user_id,))

                else:
                    query_insert_new_user = """INSERT INTO actividad (id_user, id_juego, puntaje, ult_ingreso) VALUES (%s, 2, 1, %s)"""
                    cursor.execute(query_insert_new_user, (self.user_id, datetime.datetime.now().strftime('%Y-%m-%d')))
                    query_primer_logro = "UPDATE actividad SET logro = '001' WHERE id_user = %s AND id_juego = 2"
                    cursor.execute(query_primer_logro, (self.user_id,))

                game_duration = (pygame.time.get_ticks() - self.game_start_time) // 1000
                query_update_game_time = """UPDATE actividad SET tiempo = tiempo + %s WHERE id_user = %s AND id_juego = 2"""
                cursor.execute(query_update_game_time, (game_duration, self.user_id))

                query_update_last_login = """UPDATE actividad SET ult_ingreso = %s WHERE id_user = %s AND id_juego = 2"""
                cursor.execute(query_update_last_login, (datetime.datetime.now().strftime('%Y-%m-%d'), self.user_id))

                connection.commit()
                print(f"Database updated successfully. Player won against AI. Total victories: {new_victories}")

        except mysql.connector.Error as e:
            print(f"Error de base de datos: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def draw_start_screen(self):
        self.screen.fill(self.BLACK)
        title = self.font.render("PONG", True, self.WHITE)
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 100))

        if self.game_mode == 'PLAYER_VS_PLAYER':
            controls = [
                "Controles del Jugador 1:",
                "W - Mover arriba",
                "S - Mover abajo",
                " ",
                "Controles del Jugador 2:",
                "Flecha arriba - Mover arriba",
                "Flecha abajo - Mover abajo"
            ]
        else:
            controls = [
                "Controles del Jugador:",
                "W - Mover hacia arriba",
                "S - Mover hacia abajo",
                "La IA controlara la paleta derecha"
            ]

        y_offset = 250
        for line in controls:
            control_text = self.small_font.render(line, True, self.WHITE)
            self.screen.blit(control_text, (self.WIDTH // 2 - control_text.get_width() // 2, y_offset))
            y_offset += 30

        start_text = self.menu_font.render("Presiona ENTER para comenzar", True, self.WHITE)
        self.screen.blit(start_text, (self.WIDTH // 2 - start_text.get_width() // 2, 500))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            if self.game_state == 'MENU':
                self.draw_menu()
            elif self.game_state == 'START_SCREEN':
                self.draw_start_screen()
            elif self.game_state == 'PLAYING':
                self.move_paddles()
                self.move_ball()

                if self.check_winner():
                    self.game_state = 'GAME_OVER'
                    if self.game_mode == 'PLAYER_VS_AI' and self.left_score > self.right_score:
                        self.db_config("Left Player")

                self.draw_game()
            elif self.game_state == 'GAME_OVER':
                self.draw_game_over()
            
            self.clock.tick(self.FPS)

        pygame.quit()

if __name__ == "__main__":
    user_id = sys.argv[1]
    game = Game(user_id)
    game.run()
