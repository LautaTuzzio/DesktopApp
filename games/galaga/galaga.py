import pygame
import sys
import os
import math
import random
import mysql.connector
from mysql.connector import Error
import datetime
import time

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()  # Inicializamos el mixer para los sonidos
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galaga")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Cargar imágenes
def load_image(name, scale=1):
    fullname = os.path.join('games', 'galaga', name)
    image = pygame.image.load(fullname)
    size = image.get_size()
    scaled_size = (int(size[0] * scale), int(size[1] * scale))
    return pygame.transform.scale(image, scaled_size)

# Cargar sonidos
def load_sound(name):
    fullname = os.path.join('games', 'galaga', name)
    return pygame.mixer.Sound(fullname)

player_img = load_image('nave.png', 0.5)
enemy_img = load_image('malo.png', 0.5)
bullet_img = load_image('bala.png', 0.5)
bulleta_img = load_image('balaAzul.png', 0.5)
life_img = load_image('vida.png', 0.05)
shoot_sound = load_sound('shoot.wav')
explosion_sound = load_sound('explosion.wav')

# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = player_img
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed = 5
        self.lives = 3
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.can_shoot = False
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.total_time = datetime.timedelta()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed

        if self.invulnerable:
            # Ajustar la opacidad durante la invulnerabilidad
            alpha = 128 + int(127 * math.sin(pygame.time.get_ticks() * 0.01))
            self.image = self.original_image.copy()
            self.image.set_alpha(alpha)
            
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.image = self.original_image
        else:
            self.image = self.original_image

    def shoot(self):
        if self.can_shoot:
            shoot_sound.play()
            return Bullet(self.rect.centerx, self.rect.top, -10, bullet_img)
        return None

    def hit(self):
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = 90
            print(f"Vidas restantes: {self.lives}")
    def update_database(self, final_score, game_over=False):
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
                user_id = sys.argv[1]

                # Calcular tiempo de juego
                current_time = time.time()
                session_duration = int(current_time - self.last_update_time)
                self.last_update_time = current_time
                
                # Convertir a formato tiempo
                hours, remainder = divmod(session_duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_format = f"{hours:02}:{minutes:02}:{seconds:02}"

                # Verificar registro existente
                query_check_user = "SELECT puntaje, logro, tiempo FROM actividad WHERE id_user = %s AND id_juego = 4"
                cursor.execute(query_check_user, (user_id,))
                result = cursor.fetchone()

                if result:
                    current_score = result[0]
                    current_logro = result[1]
                    current_time = result[2] if result[2] else datetime.timedelta()

                    # Actualizar puntuación si es mayor
                    if final_score > current_score:
                        cursor.execute("UPDATE actividad SET puntaje = %s WHERE id_user = %s AND id_juego = 4",
                                     (final_score, user_id))

                    # Actualizar tiempo de juego
                    query_update_time = """
                        UPDATE actividad 
                        SET tiempo = ADDTIME(tiempo, %s),
                            ult_ingreso = %s 
                        WHERE id_user = %s AND id_juego = 4
                    """
                    cursor.execute(query_update_time, (time_format, 
                                                     datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                     user_id))

                else:
                    # Crear nuevo registro
                    query_insert = """
                        INSERT INTO actividad (id_user, id_juego, puntaje, tiempo, ult_ingreso, logro) 
                        VALUES (%s, 4, %s, %s, %s, '000')
                    """
                    cursor.execute(query_insert, (user_id, final_score, time_format, 
                                               datetime.datetime.now().strftime('%Y-%m-%d')))

                connection.commit()

        except mysql.connector.Error as e:
            print(f"Error en la base de datos: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_achievements(self, level):
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
                user_id = sys.argv[1]

                # Obtener logro actual
                cursor.execute("SELECT logro FROM actividad WHERE id_user = %s AND id_juego = 4", (user_id,))
                result = cursor.fetchone()
                current_logro = str(result[0]) if result else '000'  # Convert to string explicitly

                # Obtener monedas actuales
                cursor.execute("SELECT monedas FROM usuario WHERE id_user = %s", (user_id,))
                result_monedas = cursor.fetchone()
                monedas = result_monedas[0] if result_monedas else 0

                # Convertir current_logro a número para comparación
                logro_num = int(current_logro)

                # Actualizar logros basados en el nivel
                if level >= 1 and logro_num < 1:
                    cursor.execute("UPDATE actividad SET logro = '001' WHERE id_user = %s AND id_juego = 4", (user_id,))
                    monedas += 1000
                elif level >= 10 and logro_num < 11:
                    cursor.execute("UPDATE actividad SET logro = '011' WHERE id_user = %s AND id_juego = 4", (user_id,))
                    monedas += 3000
                elif level >= 20 and logro_num < 111:
                    cursor.execute("UPDATE actividad SET logro = '111' WHERE id_user = %s AND id_juego = 4", (user_id,))
                    monedas += 10000

                # Actualizar monedas
                cursor.execute("UPDATE usuario SET monedas = %s WHERE id_user = %s", (monedas, user_id))
                connection.commit()

        except mysql.connector.Error as e:
            print(f"Error en la base de datos: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, formation_index, level, formation):  # Add formation parameter
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x
        self.original_y = y
        self.formation_index = formation_index
        self.state = "entering"
        self.path = []
        self.path_index = 0
        self.speed = 2 + (level - 1) * 0.5
        self.health = 1 + (level // 5)
        self.formation = formation  # Store formation reference

    def update(self, formation_offset_x):
        if self.state == "entering":
            if self.path_index < len(self.path):
                target_x, target_y = self.path[self.path_index]
                dx = target_x - self.rect.x
                dy = target_y - self.rect.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > self.speed:
                    self.rect.x += (dx / distance) * self.speed
                    self.rect.y += (dy / distance) * self.speed
                else:
                    self.rect.x = target_x
                    self.rect.y = target_y
                    self.path_index += 1
            else:
                self.state = "formation"
        elif self.state == "formation":
            self.rect.x = self.original_x + formation_offset_x
        elif self.state == "attacking":
            if self.path_index < len(self.path):
                target_x, target_y = self.path[self.path_index]
                dx = target_x - self.rect.x
                dy = target_y - self.rect.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > self.speed:
                    self.rect.x += (dx / distance) * self.speed
                    self.rect.y += (dy / distance) * self.speed
                else:
                    self.rect.x = target_x
                    self.rect.y = target_y
                    self.path_index += 1
            else:
                # En lugar de kill(), volvemos a la formación
                self.state = "entering"
                self.path = self.formation.generate_entry_path(self.original_x, self.original_y)  # Use formation reference
                self.path_index = 0
                self.rect.y = -50  # Posicionamos la nave arriba de la pantalla

    def start_attack(self, player_x):
        self.state = "attacking"
        self.path = self.generate_attack_path(player_x)
        self.path_index = 0

    def generate_attack_path(self, player_x):
        path = []
        start_x, start_y = self.rect.x, self.rect.y
        end_x = player_x
        end_y = height + 50
        
        for i in range(20):
            t = i / 19
            x = start_x + (end_x - start_x) * t
            y = start_y + (end_y - start_y) * (t ** 2)
            path.append((int(x), int(y)))
        
        return path

    def set_entry_path(self, path):
        self.path = path
        self.path_index = 0

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.bottom, 5, bulleta_img)

class EnemyFormation:
    def __init__(self, all_sprites_group, player):
        self.enemies = pygame.sprite.Group()
        self.offset_x = 0
        self.direction = 1
        self.speed = 0.5
        self.formation_complete = False
        self.all_sprites = all_sprites_group
        self.player = player  # Store player reference

    def create_enemies(self, level):
        self.enemies.empty()
        self.formation_complete = False
        num_enemies = 30 if level % 5 == 0 else 20
        rows = 4 if num_enemies == 20 else 5
        cols = 5 if num_enemies == 20 else 6
        
        for row in range(rows):
            for col in range(cols):
                x = 250 + col * 50
                y = 50 + row * 50
                enemy = Enemy(x, y, row * cols + col, level, self)  # Pass self as formation
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        self.set_entry_paths()

    def set_entry_paths(self):
        for enemy in self.enemies:
            path = self.generate_entry_path(enemy.rect.x, enemy.rect.y)
            enemy.set_entry_path(path)

    def generate_entry_path(self, end_x, end_y):
        path = []
        start_x = random.randint(0, width)
        start_y = -10
        control_x = random.randint(0, width)
        control_y = random.randint(0, end_y)
        
        for i in range(30):
            t = i / 29
            x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * end_y
            path.append((int(x), int(y)))
        
        return path

    def update(self):
        self.offset_x += self.speed * self.direction
        if abs(self.offset_x) > 50:
            self.direction *= -1

        all_in_formation = True
        for enemy in self.enemies:
            enemy.update(self.offset_x)
            if enemy.state != "formation":
                all_in_formation = False

        if all_in_formation and not self.formation_complete:
            self.formation_complete = True
            self.player.can_shoot = True  # Use the stored player reference

    def get_attackers(self, num_attackers):
        attackers = [e for e in self.enemies if e.state == "formation"]
        if len(attackers) > num_attackers:
            return random.sample(attackers, num_attackers)
        return attackers

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > height:
            self.kill()

def main_game():
    # Variables de juego
    score = 0
    level = 1
    game_over = False
    restart_prompt = False
    
    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    
    # Crear jugador y formación de enemigos
    player = Player()
    all_sprites.add(player)
    enemy_formation = EnemyFormation(all_sprites, player)  # Pass player instance here
    enemy_formation.create_enemies(level)
    
    # Temporizadores
    attack_timer = 0
    enemy_shoot_timer = 0
    
    # Fuente
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Bucle principal
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.update_database(score, True)
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bullet = player.shoot()
                    if bullet:
                        all_sprites.add(bullet)
                        player_bullets.add(bullet)
                elif event.key == pygame.K_r and game_over:
                    return True

        if not game_over:
            # Actualización de elementos del juego
            player.update()
            enemy_formation.update()
            player_bullets.update()
            enemy_bullets.update()

            # Gestión de ataques enemigos
            if enemy_formation.formation_complete:
                attack_timer += 1
                if attack_timer >= max(60, 180 - level * 5):
                    attack_timer = 0
                    num_attackers = min(2 + level // 3, 5)
                    attackers = enemy_formation.get_attackers(num_attackers)
                    for attacker in attackers:
                        attacker.start_attack(player.rect.centerx)

                enemy_shoot_timer += 1
                if enemy_shoot_timer >= max(30, 90 - level * 2):
                    enemy_shoot_timer = 0
                    if enemy_formation.enemies:
                        shooting_enemy = random.choice(enemy_formation.enemies.sprites())
                        bullet = shooting_enemy.shoot()
                        all_sprites.add(bullet)
                        enemy_bullets.add(bullet)

            # Colisiones
            hits = pygame.sprite.groupcollide(enemy_formation.enemies, player_bullets, False, True)
            for enemy in hits:
                enemy.health -= 1
                if enemy.health <= 0:
                    explosion_sound.play()
                    enemy.kill()
                    score += 10 * level

            pygame.sprite.groupcollide(player_bullets, enemy_bullets, True, True)

            if (pygame.sprite.spritecollide(player, enemy_formation.enemies, True) or 
                pygame.sprite.spritecollide(player, enemy_bullets, True)) and not player.invulnerable:
                player.hit()
                if player.lives <= 0:
                    game_over = True
                    player.update_database(score)

            # Verificar victoria del nivel
            if len(enemy_formation.enemies) == 0:
                level += 1
                player.can_shoot = False
                enemy_formation.create_enemies(level)
                player.update_achievements(level)

        # Dibujo
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Mostrar información del juego
        score_text = font.render(f"Puntaje: {score}", True, WHITE)
        level_text = font.render(f"Nivel: {level}", True, WHITE)
        controls_text = small_font.render("<- -> Para moverse, Espacio para disparar", True, GRAY)
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (width // 2 - 40, 10))
        screen.blit(controls_text, (10, height - 30))

        # Dibujar vidas
        for i in range(player.lives):
            screen.blit(life_img, (width - 35 - (i * 40), 10))

        if game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            final_score_text = font.render(f"Puntuacion Final: {score}", True, WHITE)
            restart_text = font.render("Presiona R para reiniciar", True, WHITE)
            
            screen.blit(game_over_text, (width // 2 - 70, height // 2 - 50))
            screen.blit(final_score_text, (width // 2 - 70, height // 2))
            screen.blit(restart_text, (width // 2 - 70, height // 2 + 50))

        pygame.display.flip()
        clock.tick(60)

        # Actualizar base de datos periódicamente
        if not game_over and time.time() - player.last_update_time >= 60:  # Actualizar cada minuto
            player.update_database(score)

    return False

# Bucle principal del programa
while main_game():
    pass

pygame.quit()
sys.exit()
