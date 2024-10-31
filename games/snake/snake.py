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
body = "games\snake\images\snakebody1.jpg"
Head = "games\snake\images\SnakeHead"

SNAKE_BODY = pygame.transform.scale(pygame.image.load(os.path.join(f"{body}")), (SNAKE_SIZE, SNAKE_SIZE))
APPLE = pygame.transform.scale(pygame.image.load(os.path.join(r"games\snake\images\manzana.png")), (APPLE_SIZE, APPLE_SIZE))
SNAKE_HEAD = []

for x in range(1, 5):
    SNAKE_HEAD.append(pygame.transform.scale(pygame.image.load(os.path.join(f"{Head}" + str(x) + ".png")), (SNAKE_SIZE, SNAKE_SIZE)))

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

    def restart(self):
        self.body = [Vector2(0, ALTO // 2), Vector2(-SNAKE_SIZE, ALTO // 2), Vector2(-2 * SNAKE_SIZE, ALTO // 2)]
        self.direction = Vector2(SNAKE_SIZE, 0)
        self.grow = False
        self.score = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_move_time = time.time()


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

                query_check_user = "SELECT puntaje, logro FROM actividad WHERE id_user = %s AND id_juego = 1"
                cursor.execute(query_check_user, (user_id,))
                result = cursor.fetchone()

                
                query_monedas = "SELECT monedas FROM usuario WHERE id_user = %s"
                cursor.execute(query_monedas, (user_id,))
                result_monedas = cursor.fetchone()

                
                if result_monedas is not None and result_monedas[0] is not None:
                    monedas = result_monedas[0]
                else:
                    monedas = 0  

                if result is not None:
                    db_score = result[0]  
                    logros = result[1]     

                  
                    if db_score <= score:
                        query_update_max_score = "UPDATE actividad SET puntaje = %s WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_update_max_score, (score, user_id))

                    # Primer logro
                    if score > 0 and logros <= 0:
                        query_primer_logro = "UPDATE actividad SET logro = '001' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_primer_logro, (user_id,))
                        if int(logros) < 1: 
                            monedas += 1000

                    # Segundo logro
                    if score >= 20 and logros < 11:
                        query_segundo_logro = "UPDATE actividad SET logro = '011' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_segundo_logro, (user_id,))
                        if int(logros) < 11:  
                            monedas += 10000

                    # Tercer logro
                    if score >= 1197 and logros < 111:
                        query_tercer_logro = "UPDATE actividad SET logro = '111' WHERE id_user = %s AND id_juego = 1"
                        cursor.execute(query_tercer_logro, (user_id,))
                        if int(logros) < 111:  
                            monedas += 50000

                else:
                    query_insert_new_user = """INSERT INTO actividad (id_user, id_juego, puntaje, tiempo, ult_ingreso) 
                                            VALUES (%s, 1, %s, 0, %s)"""
                    cursor.execute(query_insert_new_user, (user_id, score, datetime.datetime.now().strftime('%Y-%m-%d')))

                query_update_monedas = "UPDATE usuario SET monedas = %s WHERE id_user = %s"
                cursor.execute(query_update_monedas, (monedas, user_id))

                self.update_game_time(cursor, connection, user_id)

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
        font = pygame.font.SysFont('Calibri', 40)
        text = font.render('You Win!', True, (0, 255, 0))
        WIN.blit(text, (320, 240))
        pygame.display.update()
        time.sleep(2)

    def die(self):
        if self.body[0].x < 0 or self.body[0].x >= ANCHO or self.body[0].y < 0 or self.body[0].y >= ALTO:
            return True
        for bloque in self.body[1:]:
            if self.body[0] == bloque:
                return True
        return False

class Apple:
    def __init__(self):
        self.generate(None) 

    def draw(self):
        WIN.blit(APPLE, (self.pos.x, self.pos.y))

    def generate(self, snake_body):
        while True:
            self.x = random.randrange(0, ANCHO // SNAKE_SIZE)
            self.y = random.randrange(0, ALTO // SNAKE_SIZE)
            self.pos = Vector2(self.x * SNAKE_SIZE, self.y * SNAKE_SIZE)

            if snake_body is None or self.pos not in snake_body:
                break  

    def check_collision(self, snake):
        if abs(snake.body[0].x - self.pos.x) < SNAKE_SIZE and abs(snake.body[0].y - self.pos.y) < SNAKE_SIZE:
            self.generate(snake.body)  
            snake.grow = True
            return True

        for bloque in snake.body[1:]:
            if self.pos == bloque:
                self.generate(snake.body)

        return False
    

def get_skins():
    config = {
        "host": "localhost",
        "database": "desktopapp",
        "user": "root",
        "password": ""
    }
    skins = []
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()
        query_skins = "SELECT nombre FROM objetos WHERE userID = %s AND id_juego = 1 and comprado = 1"
        cursor.execute(query_skins, (user_id,))
        result = cursor.fetchall()
        skins = [skin[0] for skin in result]
        skins.append('Snake fondo gris')
        return skins

        
        

def mostrar_menu():
    opciones = ["Iniciar Juego"]
    seleccion = 0
    fuente = pygame.font.SysFont("Russo One", 40)
    fuente_instrucciones = pygame.font.SysFont("Russo One", 20)

    while True:
        WIN.fill((0, 0, 0))
        
        # Title
        titulo = fuente.render("¡SNAKE!", True, (0, 255, 0))
        WIN.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 4))

        # Instructions
        instruccion1 = fuente_instrucciones.render("Presiona enter para seleccionar", True, (200, 200, 200))
        instruccion2 = fuente_instrucciones.render("Utiliza las flechas para moverte", True, (200, 200, 200))
        WIN.blit(instruccion1, (ANCHO // 2 - instruccion1.get_width() // 2, ALTO * 3 // 4))
        WIN.blit(instruccion2, (ANCHO // 2 - instruccion2.get_width() // 2, ALTO * 3 // 4 + 30))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (100, 100, 100)
            texto = fuente.render(opcion, True, color)
            WIN.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50 + i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and seleccion > 0:
                    seleccion -= 1
                elif event.key == pygame.K_DOWN and seleccion < len(opciones) - 1:
                    seleccion += 1
                elif event.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return None

def mostrar_skins():
    skins = get_skins()
    seleccion = 0
    fuente = pygame.font.SysFont("Russo One", 40)
    fuente_instrucciones = pygame.font.SysFont("Russo One", 20)

    while True:
        WIN.fill((0, 0, 0))
        
        # Title
        titulo = fuente.render("¡SNAKE!", True, (0, 255, 0))
        WIN.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 4))

        # Instructions
        instruccion1 = fuente_instrucciones.render("Presiona enter para seleccionar", True, (200, 200, 200))
        instruccion2 = fuente_instrucciones.render("Utiliza las flechas para moverte", True, (200, 200, 200))
        WIN.blit(instruccion1, (ANCHO // 2 - instruccion1.get_width() // 2, ALTO * 3 // 4))
        WIN.blit(instruccion2, (ANCHO // 2 - instruccion2.get_width() // 2, ALTO * 3 // 4 + 30))

        for i, skin in enumerate(skins):
            color = (255, 255, 255) if i == seleccion else (100, 100, 100)
            texto = fuente.render(skin[5:].upper(), True, color)
            WIN.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50 + i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and seleccion > 0:
                    seleccion -= 1
                elif event.key == pygame.K_DOWN and seleccion < len(skins) - 1:
                    seleccion += 1
                elif event.key == pygame.K_RETURN:
                    return skins[seleccion]

def get_background(skin):
    if skin == "Snake fondo verde":
        return (144, 238, 144) 
    elif skin == "Snake fondo rojo":
        return (255, 102, 102)  
    elif skin == "Snake fondo gris":
        return (50, 50, 50)     
    return (0, 0, 0)  

def main():
    skin = mostrar_menu()
    skin = mostrar_skins()
    background=get_background(skin)
    snake = Snake()
    apple = Apple()
    score = 0
    fps = pygame.time.Clock()

    while True:
        
        fps.tick(500)

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

        WIN.fill(background)
        snake.draw()
        apple.draw()

        snake.move()

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
