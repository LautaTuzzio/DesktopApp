import pygame
import sys
import random
import math
import os

# Inicialización de Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galaga")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Cargar imágenes
def load_image(name, scale=1):
    fullname = os.path.join('games', 'galaga', name)
    image = pygame.image.load(fullname)
    size = image.get_size()
    scaled_size = (int(size[0] * scale), int(size[1] * scale))
    return pygame.transform.scale(image, scaled_size)

player_img = load_image('nave.png', 0.5)
enemy_img = load_image('malo.png', 0.5)

# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed = 5
        self.lives = 3
        self.invulnerable = False
        self.invulnerable_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed

        # Manejar invulnerabilidad temporal tras ser golpeado
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

    def hit(self):
        # Solo restar vidas si no está en estado invulnerable
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = 90  # 1.5 segundos de invulnerabilidad
            print(f"Vidas restantes: {self.lives}")

# Enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2
        self.speed_y = 0
        self.sway_direction = True  # Dirección del balanceo
        self.dropping = False       # Si el enemigo está cayendo
        self.resetting = False      # Si el enemigo está regresando a su posición inicial

    def update(self):
        # Movimiento de balanceo
        if not self.dropping and not self.resetting:
            self.rect.x += self.speed_x
            if self.rect.left <= 0 or self.rect.right >= width:
                self.speed_x *= -1  # Cambiar de dirección al chocar con los bordes
        
        # Si está cayendo, moverse hacia abajo
        if self.dropping:
            self.rect.y += self.speed_y
            # Si sale de la pantalla, se resetea
            if self.rect.top > height:
                self.dropping = False
                self.rect.y = random.randint(-100, -40)  # Reseteo de posición

    def drop(self):
        self.dropping = True
        self.speed_y = 2

# Bala (aunque los enemigos no disparan balas, se mantiene esta clase para el jugador)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('bala.png', 0.5)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Crear enemigos
for row in range(5):
    for column in range(10):
        enemy = Enemy(column * 60 + 100, row * 50 + 50)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Reloj y fuente
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Puntuación y nivel
score = 0
level = 1

# Función para reiniciar el nivel
def reset_level():
    global player, enemies, all_sprites
    player.rect.centerx = width // 2
    player.rect.bottom = height - 10
    enemies.empty()
    for row in range(5):
        for column in range(10):
            enemy = Enemy(column * 60 + 100, row * 50 + 50)
            all_sprites.add(enemy)
            enemies.add(enemy)

# Mover enemigos
def move_enemies():
    for enemy in enemies:
        # Probabilidad de que un enemigo comience a caer
        if random.random() < 0.005 and not enemy.dropping:
            enemy.drop()
        enemy.update()

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                all_sprites.add(bullet)
                player_bullets.add(bullet)

    # Actualización
    all_sprites.update()
    move_enemies()

    # Colisiones bala jugador-enemigo
    hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
    for hit in hits:
        score += 10

    # Colisiones enemigo-jugador (los enemigos matan al tocar la nave)
    if pygame.sprite.spritecollide(player, enemies, True, collided=None) and not player.invulnerable:
        player.hit()
        if player.lives <= 0:
            running = False

    # Comprobación de victoria del nivel
    if len(enemies) == 0:
        level += 1
        reset_level()

    # Dibujo
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Mostrar puntuación, vidas y nivel
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (width - 100, 10))
    screen.blit(level_text, (width // 2 - 40, 10))

    pygame.display.flip()
    clock.tick(60)

# Game Over
screen.fill(BLACK)
game_over_text = font.render("GAME OVER", True, WHITE)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (width // 2 - 70, height // 2 - 50))
screen.blit(final_score_text, (width // 2 - 70, height // 2 + 50))
pygame.display.flip()

# Esperar antes de cerrar
pygame.time.wait(3000)

pygame.quit()
sys.exit()
