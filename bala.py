import pygame
from pygame.sprite import Sprite

class Bala(Sprite):
    """Clase para gestionar las balas/láseres disparados desde la nave."""

    def __init__(self, ai_juego):
        """Crea un objeto para la bala en la posición actual de la nave."""
        super().__init__()
        self.pantalla = ai_juego.pantalla
        self.ajustes = ai_juego.ajustes
        self.color = self.ajustes.color_bala

        # Crear el rectángulo del láser y luego posicionarlo arriba de la nave
        self.rect = pygame.Rect(0, 0, self.ajustes.ancho_bala, self.ajustes.alto_bala)
        self.rect.midtop = ai_juego.nave.rect.midtop
        
        # Guardar la posición de la bala como valor decimal
        self.y = float(self.rect.y)

    def update(self):
        """Mueve la bala hacia arriba por la pantalla."""
        self.y -= self.ajustes.velocidad_bala
        self.rect.y = int(self.y)

    def draw_bullet(self):
        """Dibuja la bala en la pantalla."""
        pygame.draw.rect(self.pantalla, self.color, self.rect)