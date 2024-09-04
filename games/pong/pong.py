import pygame,sys
import random
import mysql.connector
import datetime

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Velocidad de actualización
FPS = 60
clock = pygame.time.Clock()
user_id = sys.argv[1]

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_SPEED = 7
AI_PADDLE_SPEED = 7  # Initial AI paddle speed

# Pelota
BALL_RADIUS = 10
INITIAL_BALL_SPEED_X = 5
INITIAL_BALL_SPEED_Y = 5
BALL_SPEED_INCREASE = 0.7
AI_SPEED_INCREASE = 0.1  # Amount to increase AI speed

# Paddles y bola
left_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Velocidad actual de la pelota
ball_speed_x = INITIAL_BALL_SPEED_X
ball_speed_y = INITIAL_BALL_SPEED_Y

# Puntuaciones
left_score = 0
right_score = 0

# Condiciones de victoria
WINNING_SCORE = 7
WINNING_DIFFERENCE = 2

# Fuentes
font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 36)

# Estados del juego
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Modo de juego
PLAYER_VS_PLAYER = 0
PLAYER_VS_AI = 1
game_mode = PLAYER_VS_PLAYER

# Función para mover los paddles
def move_paddles():
    global AI_PADDLE_SPEED
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    
    if game_mode == PLAYER_VS_PLAYER:
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED
    else:
        # AI movement
        if right_paddle.centery < ball.centery and right_paddle.bottom < HEIGHT:
            right_paddle.y += AI_PADDLE_SPEED
        elif right_paddle.centery > ball.centery and right_paddle.top > 0:
            right_paddle.y -= AI_PADDLE_SPEED

# Función para mover la pelota
def move_ball():
    global ball_speed_x, ball_speed_y, left_score, right_score, AI_PADDLE_SPEED
    ball.x += ball_speed_x 
    ball.y += ball_speed_y

    # Colisión con la parte superior o inferior de la pantalla
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Colisión con los paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        # Aumentar la velocidad de la pelota
        if ball_speed_x > 0:
            ball_speed_x += BALL_SPEED_INCREASE
        else:
            ball_speed_x -= BALL_SPEED_INCREASE
        if ball_speed_y > 0:
            ball_speed_y += BALL_SPEED_INCREASE
        else:
            ball_speed_y -= BALL_SPEED_INCREASE
        
        # Increase AI paddle speed
        if game_mode == PLAYER_VS_AI:
            AI_PADDLE_SPEED += AI_SPEED_INCREASE

    # Puntaje y reinicio de la pelota
    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball()

# Función para reiniciar la pelota
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = INITIAL_BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = INITIAL_BALL_SPEED_Y * random.choice((1, -1))

# Función para verificar si hay un ganador
def check_winner():
    if (left_score >= WINNING_SCORE or right_score >= WINNING_SCORE) and abs(left_score - right_score) >= WINNING_DIFFERENCE:
        return True
    return False

# Función para dibujar en pantalla
def draw_game():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    left_text = font.render(str(left_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))

    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(right_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip()

# Función para dibujar el menú
def draw_menu():
    screen.fill(BLACK)
    title = font.render("PONG", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    pvp = menu_font.render("1. Player vs Player", True, WHITE)
    screen.blit(pvp, (WIDTH // 2 - pvp.get_width() // 2, 300))

    pva = menu_font.render("2. Player vs AI", True, WHITE)
    screen.blit(pva, (WIDTH // 2 - pva.get_width() // 2, 350))

    pygame.display.flip()

def db_config(winner):
    if game_mode != PLAYER_VS_AI or winner != "Left Player":
        return  # Solo actualizamos la base de datos si el jugador gana contra la IA

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
            cursor.execute(query_check_user, (user_id,))
            result = cursor.fetchone()

            if result is not None:
                current_victories = result[0]
                new_victories = current_victories + 1
                
                query_update_victories = "UPDATE actividad SET puntaje = %s WHERE id_user = %s AND id_juego = 2"
                cursor.execute(query_update_victories, (new_victories, user_id))

                # Actualizar logros basados en el número de victorias
                if new_victories == 1:
                    query_primer_logro = "UPDATE actividad SET logro = '001' WHERE id_user = %s AND id_juego = 2"
                    cursor.execute(query_primer_logro, (user_id,))
                elif new_victories == 5:
                    query_segundo_logro = "UPDATE actividad SET logro = '011' WHERE id_user = %s AND id_juego = 2"
                    cursor.execute(query_segundo_logro, (user_id,))
                elif new_victories == 20:
                    query_tercer_logro = "UPDATE actividad SET logro = '111' WHERE id_user = %s AND id_juego = 2"
                    cursor.execute(query_tercer_logro, (user_id,))

            else:
                # Si es la primera vez que el usuario juega, insertamos un nuevo registro
                query_insert_new_user = """INSERT INTO actividad (id_user, id_juego, puntaje, tiempo, ult_ingreso) VALUES (%s, 2, 1, 0, %s)"""
                cursor.execute(query_insert_new_user, (user_id, datetime.datetime.now().strftime('%Y-%m-%d')))

            # Actualizar el tiempo de juego y el último ingreso
            query_update_game_time = """UPDATE actividad SET tiempo = tiempo + %s WHERE id_user = %s AND id_juego = 2"""
            cursor.execute(query_update_game_time, (game_duration, user_id))

            query_update_last_login = """UPDATE actividad SET ult_ingreso = %s WHERE id_user = %s AND id_juego = 2"""
            cursor.execute(query_update_last_login, (datetime.datetime.now().strftime('%Y-%m-%d'), user_id))

            connection.commit()
            print(f"Database updated successfully. Player won against AI. Total victories: {new_victories}")

    except mysql.connector.Error as e:
        print(f"Error de base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Función para dibujar la pantalla de fin del juego
def draw_game_over():
    screen.fill(BLACK)
    if left_score > right_score:
        winner_text = "Left Player Wins!"
    else:
        winner_text = "Right Player Wins!"
    winner_surface = font.render(winner_text, True, WHITE)
    screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2 - winner_surface.get_height() // 2))
    if game_mode == PLAYER_VS_AI and left_score > right_score:
        db_config("Left Player")
    play_again = menu_font.render("Press SPACE to play again", True, WHITE)
    screen.blit(play_again, (WIDTH // 2 - play_again.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()

# Función para reiniciar el juego
def reset_game():
    global left_score, right_score, game_state, AI_PADDLE_SPEED
    left_score = 0
    right_score = 0
    AI_PADDLE_SPEED = PADDLE_SPEED  # Reset AI paddle speed
    reset_ball()
    left_paddle.centery = HEIGHT // 2
    right_paddle.centery = HEIGHT // 2
    game_state = PLAYING

# Agregar variable para el tiempo de juego
game_start_time = None

# Modificar el bucle principal para manejar el tiempo de juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_1:
                    game_mode = PLAYER_VS_PLAYER
                    reset_game()
                    game_start_time = pygame.time.get_ticks()  # Iniciar el tiempo de juego
                elif event.key == pygame.K_2:
                    game_mode = PLAYER_VS_AI
                    reset_game()
                    game_start_time = pygame.time.get_ticks()  # Iniciar el tiempo de juego
            elif game_state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    game_state = MENU

    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        move_paddles()
        move_ball()

        if check_winner():
            game_state = GAME_OVER
            game_end_time = pygame.time.get_ticks()
            game_duration = (game_end_time - game_start_time) // 1000  # Duración en segundos

        draw_game()
    elif game_state == GAME_OVER:
        draw_game_over()
    
    clock.tick(FPS)

pygame.quit()