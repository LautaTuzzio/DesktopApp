import pygame
from pygame.math import Vector2 
import random
import os
import sys
import mysql.connector
from mysql.connector import Error
import datetime
import time

pygame.init()

ANCHO = 720
ALTO = 480

SNAKE_SIZE = 30
APPLE_SIZE = 30
user_id = sys.argv[1]
body="games\snake\images\snakebody1.jpg"
Head="games\snake\images\SnakeHead"


SNAKE_BODY = pygame.transform.scale(pygame.image.load(os.path.join(f"{body}")), (SNAKE_SIZE, SNAKE_SIZE))
APPLE = pygame.transform.scale(pygame.image.load(os.path.join(r"games\snake\images\manzana.png")), (APPLE_SIZE, APPLE_SIZE))
SNAKE_HEAD = []

for x in range(1, 5):
    SNAKE_HEAD.append(pygame.transform.scale(pygame.image.load(os.path.join(f"{Head}"+str(x)+".png")), (SNAKE_SIZE, SNAKE_SIZE)))

EAT_SOUND = pygame.mixer.Sound("games\snake\coin.wav")

WIN = pygame.display.set_mode((ANCHO, ALTO))

SCORE_TEXT = pygame.font.SysFont("Russo One", 25)

class Snake:
    def __init__(self):
        self.body = [Vector2(0, ALTO // 2), Vector2(-SNAKE_SIZE, ALTO // 2), Vector2(-2 * SNAKE_SIZE, ALTO // 2)]
        self.direction = Vector2(SNAKE_SIZE, 0)
        self.grow = False
        self.score = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_move_time = time.time()
        self.move_delay = 0.1

    def draw(self):
        for bloque in self.body:
            WIN.blit(SNAKE_BODY, (bloque.x, bloque.y))

        if self.direction == Vector2(0, -SNAKE_SIZE):
            WIN.blit(SNAKE_HEAD[0], (self.body[0].x, self.body[0].y))
        elif self.direction == Vector2(0, SNAKE_SIZE):
            WIN.blit(SNAKE_HEAD[2], (self.body[0].x, self.body[0].y))
        elif self.direction == Vector2(SNAKE_SIZE, 0):
            WIN.blit(SNAKE_HEAD[1], (self.body[0].x, self.body[0].y))
        elif self.direction == Vector2(-SNAKE_SIZE, 0):
            WIN.blit(SNAKE_HEAD[3], (self.body[0].x, self.body[0].y))

    def update_game_time(self, cursor, connection, user_id):
        current_time = time.time()
        elapsed_time = int(current_time - self.last_update_time)
        self.last_update_time = current_time

        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_format = f"{hours:02}:{minutes:02}:{seconds:02}"

        query_update_time = """UPDATE actividad SET tiempo = ADDTIME(tiempo, %s), ult_ingreso = %s WHERE id_user = %s AND id_juego = 1"""
        cursor.execute(query_update_time, (time_format, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        connection.commit()

    

    def scoreQuery(self, score):
        self.score = score
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

                # Consulta para obtener el puntaje del usuario en el juego
                query_check_user = "SELECT puntaje, logro FROM actividad WHERE id_user = %s AND id_juego = 1"
                cursor.execute(query_check_user, (user_id,))
                result = cursor.fetchone()

                # Consulta para obtener las monedas del usuario
                query_monedas = "SELECT monedas FROM usuario WHERE id_user = %s"
                cursor.execute(query_monedas, (user_id,))
                result_monedas = cursor.fetchone()

                # Inicialización de variables
                if result_monedas is not None and result_monedas[0] is not None:
                    monedas = result_monedas[0]
                else:
                    monedas = 0  # Inicializa monedas a 0 si no hay datos

                if result is not None:
                    db_score = result[0]  # Puntaje almacenado en la base de datos
                    logros = result[1]     # Logros almacenados en la base de datos

                    # Si el puntaje actual es mayor que el puntaje en la base de datos, actualiza el puntaje
                    if db_score <= score:
                        query_update_max_score = "UPDATE actividad SET puntaje = %s WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_update_max_score, (score, user_id))

                    # Primer logro
                    if score > 0:
                        query_primer_logro = "UPDATE actividad SET logro = '001' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_primer_logro, (user_id,))
                        if int(logros) < 1:  # Verifica si el logro es menor que 1
                            monedas += 1000

                    # Segundo logro
                    if score >= 20:
                        query_segundo_logro = "UPDATE actividad SET logro = '011' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_segundo_logro, (user_id,))
                        if int(logros) < 11:  # Verifica si el logro es menor que 11
                            monedas += 10000

                    # Tercer logro
                    if score >= 1197:
                        query_tercer_logro = "UPDATE actividad SET logro = '111' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_tercer_logro, (user_id,))
                        if int(logros) < 111:  # Verifica si el logro es menor que 111
                            monedas += 50000

                else:
                    # Si no existe el usuario en la tabla actividad, lo inserta
                    query_insert_new_user = """INSERT INTO actividad (id_user, id_juego, puntaje, tiempo, ult_ingreso) 
                                            VALUES (%s, 1, %s, 0, %s)"""
                    cursor.execute(query_insert_new_user, (user_id, score, datetime.datetime.now().strftime('%Y-%m-%d')))

                # Actualiza las monedas del usuario
                query_update_monedas = "UPDATE usuario SET monedas = %s WHERE id_user = %s"
                cursor.execute(query_update_monedas, (monedas, user_id))

                # Actualiza el tiempo de juego
                self.update_game_time(cursor, connection, user_id)

                # Actualiza el último ingreso
                query_update_last_login = """UPDATE actividad SET ult_ingreso = %s WHERE id_user = %s AND id_juego = 1"""
                cursor.execute(query_update_last_login, (datetime.datetime.now().strftime('%Y-%m-%d'), user_id))
                connection.commit()

        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def can_move(self):
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_delay:
            self.last_move_time = current_time
            return True
        return False

    def move(self):
        if self.can_move():
            self._perform_move()

    def _perform_move(self):
        if self.grow:
            self.body.insert(0, self.body[0] + self.direction)
            self.grow = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy

    def instant_move(self, new_direction):
        if self.direction != new_direction and self.direction != -new_direction:
            self.direction = new_direction
            self._perform_move()
            self.last_move_time = time.time()  # Reset the move timer

    def pause(self):
        DieFont = pygame.font.SysFont('Calibri', 40)
        restartFont = pygame.font.SysFont('Calibri', 20)

        text_die = DieFont.render("Game Over", True, (255, 255, 255))
        WIN.blit(text_die, (290, 170))
            
        text_die_restart = restartFont.render("Space to restart", True, (255, 255, 255))
        WIN.blit(text_die_restart, (310, 210))

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

    def winscreen(self):
        WIN.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 64)
        victory_text = font.render("¡Congratulations! you win", True, (0, 0, 0))
        score_text = font.render(f"score: 384", True, (0, 0, 0))
        play_again_text = font.render("Press space to play again", True, (0, 0, 0))
        
        WIN.blit(victory_text, (ANCHO // 2 - victory_text.get_width() // 2, ALTO // 2 - 100))
        WIN.blit(score_text, (ANCHO // 2 - score_text.get_width() // 2, ALTO // 2 - 30))
        WIN.blit(play_again_text, (ANCHO // 2 - play_again_text.get_width() // 2, ALTO // 2 + 40))

        pygame.display.update()

        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart()
                        paused = False
                        return 

    def restart(self):
        self.body = [Vector2(0, ALTO // 2), Vector2(-SNAKE_SIZE, ALTO // 2), Vector2(-2 * SNAKE_SIZE, ALTO // 2)]
        self.direction = Vector2(SNAKE_SIZE, 0)
        self.score = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_move_time = time.time()

        return self.score

    def die(self):
        if self.body[0].x >= ANCHO or self.body[0].y >= ALTO or self.body[0].x < 0 or self.body[0].y < 0:
            return True

        if self.body[0] in self.body[1:]:
            return True

        return False

class Apple:
    def __init__(self):
        self.generate()

    def draw(self):
        WIN.blit(APPLE, (self.pos.x, self.pos.y))

    def generate(self):
        self.x = random.randrange(0, ANCHO // SNAKE_SIZE)
        self.y = random.randrange(0, ALTO // SNAKE_SIZE)
        self.pos = Vector2(self.x * SNAKE_SIZE, self.y * SNAKE_SIZE)

    def check_collision(self, snake):
        if abs(snake.body[0].x - self.pos.x) < SNAKE_SIZE and abs(snake.body[0].y - self.pos.y) < SNAKE_SIZE:
            self.generate()
            snake.grow = True
            return True

        for bloque in snake.body[1:]:
            if self.pos == bloque:
                self.generate()

        return False

def get_background():
    config = {
        "host": "localhost",
        "database": "desktopapp",
        "user": "root",
        "password": ""
    }
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query_skin = "SELECT estilos FROM actividad WHERE id_user = %s AND id_juego = 1"
        cursor.execute(query_skin, (user_id,))
        result = cursor.fetchone()

        
        if result is None or result[0] is None:
            return (0, 0, 0)  
        elif result[0] == 1:
            return (144, 238, 144)
        elif result[0] == 2:
            return (255, 102, 102)
        else:
            return (50, 50, 50)

    except mysql.connector.Error as e:
        print(f"Error en la conexión a la base de datos: {e}")
        return (0, 0, 0)  

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def main():
    snake = Snake()
    apple = Apple()
    score = 0
    fps = pygame.time.Clock()
    background=get_background()
    
    while True:
        fps.tick(500)  # Mantenemos un alto FPS para una mejor respuesta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction.y != SNAKE_SIZE:
                    snake.instant_move(Vector2(0, -SNAKE_SIZE))
                elif event.key == pygame.K_DOWN and snake.direction.y != -SNAKE_SIZE:
                    snake.instant_move(Vector2(0, SNAKE_SIZE))
                elif event.key == pygame.K_RIGHT and snake.direction.x != -SNAKE_SIZE:
                    snake.instant_move(Vector2(SNAKE_SIZE, 0))
                elif event.key == pygame.K_LEFT and snake.direction.x != SNAKE_SIZE:
                    snake.instant_move(Vector2(-SNAKE_SIZE, 0))
        

        

        WIN.fill((background))
        snake.draw()
        apple.draw()

        snake.move()  # This will now only move the snake if enough time has passed

        if apple.check_collision(snake):
            score += 1
            EAT_SOUND.play()

        if score >= 384:
            snake.winscreen()
            score = 0
            continue

        if snake.die():
            snake.scoreQuery(score)
            score = 0 
            snake.pause()

        text = SCORE_TEXT.render("Score: {}".format(score), 1, (255, 255, 255))
        WIN.blit(text, (ANCHO - text.get_width() - 20, 20))

        pygame.display.update()

if __name__ == "__main__":
    main()
