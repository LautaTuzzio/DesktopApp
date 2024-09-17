import pygame, sys

pygame.init()
fps = 30
clock = pygame.time.Clock()
height = 480
width = 720
pantalla = pygame.display.set_mode((width, height))
pygame.display.set_caption('Galaga')
icono = pygame.image.load('nave.png')
pygame.display.set_icon(icono)
bala_imagen = pygame.image.load('bala.png')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = icono
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, 400)
        self.velocidad_x = 0
        self.velocidad = 7  # Velocidad de desplazamiento
        self.balas = pygame.sprite.Group()  # Grupo para las balas

    def update(self):
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -self.velocidad
        elif teclas[pygame.K_RIGHT]:
            self.velocidad_x = self.velocidad
        else:
            self.velocidad_x = 0  # Detener la nave si no hay tecla presionada
        
        self.rect.x += self.velocidad_x

        # Previene que la nave salga de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

        # Actualizar las balas
        self.balas.update()

    def disparar(self):
        nueva_bala = Bullet(self.rect.centerx, self.rect.top)
        self.balas.add(nueva_bala)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bala_imagen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = -10  # Velocidad de la bala hacia arriba

    def update(self):
        self.rect.y += self.velocidad  # Mover la bala hacia arriba

sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

# Bucle principal del juego
while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()  # Disparar una bala

    sprites.update()
    pantalla.fill((0, 0, 0))
    sprites.draw(pantalla)
    player.balas.draw(pantalla)  # Dibujar las balas
    pygame.display.update()