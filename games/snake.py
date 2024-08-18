import pygame,sys
from pygame.math import Vector2
import random
import mysql.connector
from mysql.connector import Error
import time
pygame.init()
height = 480
width = 720

win = pygame.display.set_mode((width, height))
score_text = pygame.font.SysFont("Russo One",15)

class Snake:
    def __init__(self):
        self.body = [Vector2(10, 100), Vector2(10, 110), Vector2(10, 120), Vector2(10, 120)]
        self.direction = Vector2(10, 0)
        self.add = False

    def draw(self):
        for bloque in self.body:
            pygame.draw.rect(win, (0, 255, 0), (bloque.x, bloque.y, 10, 10))

    def move(self):
        if self.add == True:
            body_copy = self.body
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.add=False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def move_up(self):
        self.direction = Vector2(0, -10)
        
    def move_down(self):
        self.direction = Vector2(0, 10)

    def move_left(self):
        self.direction = Vector2(-10, 0)

    def move_right(self):
        self.direction = Vector2(10, 0)

    def die(self):
        print(self.body[0])
        if self.body[0].x == width or self.body[0].y == height or self.body[0].x <= -10  or self.body[0].y <= -10:
            return True

        for i in self.body[1:]:
            if self.body[0] == i:
                return True
            
    def checkwin(self,score):
        if score == ((height/10)+(width/10)):
            return True


def pause():
    DieFont = pygame.font.SysFont('Calibri',40)
    restartFont = pygame.font.SysFont('Calibri',20)

    text_die = DieFont.render("Game Over",True,(255,255,255))
    win.blit(text_die,(260,200))
        
    text_die_restart = restartFont.render("Space to restart",True,(255,255,255))
    win.blit(text_die_restart,(280,240))

    pygame.display.update()
    paused=True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart()
                    paused = False
    return restart()

def restart():
    score=0
    apple = Apple()
    snake = Snake()
    fps = pygame.time.Clock()   
    return score,apple,snake,fps
    
class Apple:
    def __init__(self):
        self.generate()

    def draw(self):
        pygame.draw.rect(win, (255, 0, 0), (self.pos.x, self.pos.y, 10, 10))

    def generate(self):
        self.x = random.randrange(0, int(width / 10))
        self.y = random.randrange(0, int(height / 10))
        self.pos = Vector2(self.x*10, self.y*10)

    def check_collision(self,snake):
        if snake.body[0]==self.pos:
            self.generate()
            snake.add = True
            return True
        for block in snake.body[1:]:
            if block == self.pos:
                self.generate()

def main():
    score=0
    max_score=0
    apple = Apple()
    snake = Snake()
    fps = pygame.time.Clock()

    while True:
        fps.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN and snake.direction.y != 10:
                if event.key == pygame.K_UP:
                    snake.move_up()

            if event.type == pygame.KEYDOWN and snake.direction.y != -10:
                if event.key == pygame.K_DOWN:
                    snake.move_down()

            if event.type == pygame.KEYDOWN and snake.direction.x != -10:
                if event.key == pygame.K_RIGHT:
                    snake.move_right()

            if event.type == pygame.KEYDOWN and snake.direction.x != 10:
                if event.key == pygame.K_LEFT:
                    snake.move_left()

        win.fill((0, 0, 0))
        snake.draw()
        snake.move()
        apple.draw()

        if snake.die():
            #conexion base de datos 
            host = 'localhost'
            database = 'desktopapp'
            user = 'root'
            password = ''
            try:
                
                connection = mysql.connector.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=password
                ) 
                if connection.is_connected():
                    cursor = connection.cursor()
                    try:
                        cursor.execute("SELECT * FROM puntajes;")
                        for row in cursor.fetchall():
                            print(row[1])
                            if score > row[1]:
                                query_update=f"UPDATE puntajes SET score = '{score}' WHERE 1;" #where id usuario = current_id & game id = game id
                                cursor.execute(query_update)
                                connection.commit()
                    except Error as e:
                        print(f"Error al ejecutar la consulta: {e}")
                    finally:
                        cursor.close()
                        connection.close()
            except Error as e:
                print(f"Error al conectar a MySQL: {e}")
            
            score,apple,snake,fps=pause()
            

        if apple.check_collision(snake):
            score+=1

        if snake.checkwin(score)==True:
            print("ganaste")
            
        text = score_text.render("Score: {}".format(score),True,(255,255,255))
        win.blit(text,(10,10))
        
        pygame.display.update()

main()