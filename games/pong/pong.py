import pygame
import random

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

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_SPEED = 7

# Pelota
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Paddles y bola
left_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Puntuaciones
left_score = 0
right_score = 0

# Condiciones de victoria
WINNING_SCORE = 7
WINNING_DIFFERENCE = 2

# Fuente
font = pygame.font.Font(None, 74)

# Función para mover los paddles
def move_paddles():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

# Función para mover la pelota
def move_ball():
    global BALL_SPEED_X, BALL_SPEED_Y, left_score, right_score
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Colisión con la parte superior o inferior de la pantalla
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1

    # Colisión con los paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        BALL_SPEED_X *= -1

    # Puntaje y reinicio de la pelota
    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball()

# Función para reiniciar la pelota
def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    BALL_SPEED_X *= random.choice((1, -1))
    BALL_SPEED_Y *= random.choice((1, -1))

# Función para verificar si hay un ganador
def check_winner():
    if (left_score >= WINNING_SCORE or right_score >= WINNING_SCORE) and abs(left_score - right_score) >= WINNING_DIFFERENCE:
        return True
    return False

# Función para dibujar en pantalla
def draw():
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

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_paddles()
    move_ball()

    if check_winner():
        running = False  # Finaliza el juego si hay un ganador

    draw()
    
    clock.tick(FPS)

# Mostrar mensaje de fin del juego
if left_score > right_score:
    winner_text = "Left Player Wins!"
else:
    winner_text = "Right Player Wins!"

# Mostrar el ganador en pantalla por 3 segundos
screen.fill(BLACK)
winner_surface = font.render(winner_text, True, WHITE)
screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2 - winner_surface.get_height() // 2))
pygame.display.flip()
pygame.time.delay(3000)

pygame.quit()
