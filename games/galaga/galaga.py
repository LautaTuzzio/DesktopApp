import pygame
import sys
import random

# Inicializa Pygame
pygame.init()

# Configuración de FPS y reloj
fps = 30
clock = pygame.time.Clock()

# Dimensiones de la pantalla
height = 480
width = 720
pantalla = pygame.display.set_mode((width, height))
pygame.display.set_caption('Galaga')

# Función para cargar y escalar imágenes
def cargar_y_escalar(nombre_archivo, escala=0.5):
    imagen = pygame.image.load(nombre_archivo)
    nuevo_tamaño = (int(imagen.get_width() * escala), int(imagen.get_height() * escala))
    return pygame.transform.scale(imagen, nuevo_tamaño)

# Carga de imágenes de sprites
icono = cargar_y_escalar('nave.png')
bala_imagen = cargar_y_escalar('bala.png')
enemigo_imagen = cargar_y_escalar('malo.png')
bala_enemigo_imagen = cargar_y_escalar('bala.png', 0.3)
vida_imagen = cargar_y_escalar('vida.png')

# Establece el ícono de la ventana
pygame.display.set_icon(icono)

# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = icono
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 50)
        self.velocidad_x = 0
        self.velocidad = 7
        self.balas = pygame.sprite.Group()  # Grupo para las balas del jugador
        self.vidas = 3  # Vidas del jugador
        self.invulnerable = False  # Estado de invulnerabilidad
        self.tiempo_invulnerable = 0  # Temporizador de invulnerabilidad

    def update(self):
        teclas = pygame.key.get_pressed()
        
        # Movimiento del jugador
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -self.velocidad
        elif teclas[pygame.K_RIGHT]:
            self.velocidad_x = self.velocidad
        else:
            self.velocidad_x = 0
        
        self.rect.x += self.velocidad_x

        # Limitar movimiento dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

        self.balas.update()

        # Control de invulnerabilidad
        if self.invulnerable:
            self.tiempo_invulnerable -= 1
            if self.tiempo_invulnerable <= 0:
                self.invulnerable = False

    def disparar(self):
        nueva_bala = Bullet(self.rect.centerx, self.rect.top)
        self.balas.add(nueva_bala)  # Agregar la nueva bala al grupo

    def golpeado(self):
        if not self.invulnerable:  # Si no es invulnerable, pierde una vida
            self.vidas -= 1
            self.invulnerable = True
            self.tiempo_invulnerable = 90  # Temporizador de invulnerabilidad

# Clase para las balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad=-10, imagen=bala_imagen):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = velocidad  # Velocidad de la bala

    def update(self):
        self.rect.y += self.velocidad  # Mueve la bala hacia arriba
        if self.rect.bottom < 0 or self.rect.top > height:
            self.kill()  # Elimina la bala si sale de la pantalla

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemigo_imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.contador_disparo = 0  # Contador para controlar el disparo

    def update(self):
        self.contador_disparo += 1
        if self.contador_disparo >= 60:  # Dispara cada 60 frames
            self.disparar()
            self.contador_disparo = 0

    def disparar(self):
        nueva_bala = Bullet(self.rect.centerx, self.rect.bottom, 3, bala_enemigo_imagen)  # Dispara más lento
        return nueva_bala  # Devuelve una nueva bala enemiga

# Clase para la flota de enemigos
class EnemyFleet:
    def __init__(self):
        self.enemies = pygame.sprite.Group()  # Grupo de enemigos
        self.velocidad = 2  # Velocidad de movimiento de los enemigos
        self.direccion = 1  # Dirección del movimiento (1: derecha, -1: izquierda)
        self.limite_descenso = height * 0.6  # Límite de descenso
        self.crear_flota()

    def crear_flota(self):
        # Crea una flota de enemigos en filas y columnas
        for fila in range(3):
            for columna in range(10):
                enemy = Enemy(columna * 60 + 50, fila * 50 + 50)
                self.enemies.add(enemy)

    def update(self):
        self.enemies.update()  # Actualiza el estado de todos los enemigos
        
        for enemy in self.enemies:
            if enemy.rect.bottom < self.limite_descenso:  # Mueve los enemigos hacia abajo
                enemy.rect.y += self.velocidad
            else:
                # Cambia la dirección de los enemigos
                enemy.rect.x += self.velocidad * self.direccion
                if enemy.rect.right >= width or enemy.rect.left <= 0:
                    self.direccion *= -1
                    break

# Función para mostrar texto en pantalla
def mostrar_texto(superficie, texto, tamaño, x, y):
    font = pygame.font.Font(None, tamaño)
    texto_superficie = font.render(texto, True, (255, 255, 255))
    texto_rect = texto_superficie.get_rect()
    texto_rect.midtop = (x, y)
    superficie.blit(texto_superficie, texto_rect)

# Función para la pantalla de inicio
def pantalla_inicio():
    pantalla.fill((0, 0, 0))
    mostrar_texto(pantalla, "Galaga", 64, width // 2, height // 4)
    mostrar_texto(pantalla, "Presiona cualquier tecla para comenzar", 22, width // 2, height // 2)
    pygame.display.flip()
    esperando = True
    while esperando:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                esperando = False

# Función para la pantalla de fin de juego
def pantalla_fin(mensaje):
    pantalla.fill((0, 0, 0))
    mostrar_texto(pantalla, mensaje, 64, width // 2, height // 4)
    mostrar_texto(pantalla, "Presiona R para reiniciar o Q para salir", 22, width // 2, height // 2)
    pygame.display.flip()
    esperando = True
    while esperando:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    return True  # Reiniciar el juego
                elif event.key == pygame.K_q:
                    return False  # Salir del juego

# Función principal del juego
def juego():
    player = Player()  # Crea un jugador
    fleet = EnemyFleet()  # Crea la flota de enemigos
    sprites = pygame.sprite.Group(player)  # Grupo de sprites para el jugador
    balas_enemigas = pygame.sprite.Group()  # Grupo para las balas enemigas

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.disparar()  # Dispara al presionar espacio

        sprites.update()  # Actualiza los sprites
        fleet.update()  # Actualiza la flota de enemigos
        balas_enemigas.update()  # Actualiza las balas enemigas
        
        # Generar balas enemigas aleatorias
        for enemy in fleet.enemies:
            if random.randint(1, 200) == 1:  # Probabilidad de disparo
                balas_enemigas.add(enemy.disparar())
        
        # Colisiones entre balas del jugador y enemigos
        hits = pygame.sprite.groupcollide(fleet.enemies, player.balas, True, True)
        
        # Colisiones entre balas enemigas y jugador
        if pygame.sprite.spritecollide(player, balas_enemigas, True):
            player.golpeado()  # El jugador es golpeado
            if player.vidas <= 0:
                return "Game Over"

        # Colisiones entre balas enemigas y balas del jugador
        pygame.sprite.groupcollide(balas_enemigas, player.balas, True, True)

        # Condición de victoria
        if len(fleet.enemies) == 0:
            return "Winner!"

        pantalla.fill((0, 0, 0))  # Limpia la pantalla
        sprites.draw(pantalla)  # Dibuja al jugador
        fleet.enemies.draw(pantalla)  # Dibuja los enemigos
        player.balas.draw(pantalla)  # Dibuja las balas del jugador
        balas_enemigas.draw(pantalla)  # Dibuja las balas enemigas

        # Mostrar vidas en la esquina superior izquierda
        for i in range(player.vidas):
            pantalla.blit(pygame.transform.scale(vida_imagen, (15, 15)), (10 + i * 20, 10))  # Tamaño reducido

        if player.invulnerable:
            player.image.set_alpha(128)
        else:
            player.image.set_alpha(255)

        pygame.display.flip()  # Actualiza la pantalla

# Bucle principal del juego
while True:
    pantalla_inicio()  # Muestra la pantalla de inicio
    resultado = juego()  # Inicia el juego
    if resultado:
        continuar = pantalla_fin(resultado)  # Muestra la pantalla de fin
        if not continuar:
            break  # Sale si el jugador decide no reiniciar
    else:
        break  # Sale si se cierra el juego

pygame.quit()  # Cierra Pygame
sys.exit()  # Sale del sistema
