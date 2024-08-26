import pygame, sys
from pygame.math import Vector2
import random
import mysql.connector
from mysql.connector import Error
import time
import datetime

pygame.init()
fps=30
clock = pygame.time.Clock()
height = 480
width = 720
pantalla = pygame.display.set_mode((width,height))
pygame.display.set_caption('Galaga')
icono = pygame.image.load('nave.png')
pygame.display.set_icon(icono)

class Player(pygame.sprite.Sprite):
     def __init__(self):
          super().__init__()
          self.image = icono
          self.rect = self.image.get_rect()
          self.rect.center = (width // 2, 400)
          self.velocidad = 0 
          self.velocidad_x = 0

     def update(self):
         self.rect.x -= 10
         if self.rect.right < 0:
             self.rect.left = width
         if self.rect.left < width:
             self.rect.right = 0

         self.velocidad_x = 0

         teclas = pygame.key.get_pressed()

         if teclas[pygame.K_a]:
             self.velocidad_x = -10
         if teclas[pygame.K_d]:
              self.velocidad_x = 10

         self.rect.x += self.velocidad_x



sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)



while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            pygame.display.update()

        sprites.update()
        pantalla.fill((0,0,0))
        sprites.draw(pantalla)