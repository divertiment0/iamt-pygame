import pygame
from pygame.sprite import Sprite

class Alienigena(Sprite):
    """Una clase para representar un solo alienígena completamente animado."""

    def __init__(self, ai_juego):
        """Inicializa el alienígena y prepara sus secuencias de animación."""
        super().__init__()
        self.pantalla = ai_juego.pantalla
        self.ajustes = ai_juego.ajustes

        # 🎞️ Secuencia de fotogramas para caminar
        rutas_caminar = [
            'images/IDLE.PNG',
            'images/1ST FRAME.PNG',
            'images/WALK_1.PNG',
            'images/WALK_2.PNG'
        ]
        self.sprites_caminar = [pygame.transform.scale(pygame.image.load(r).convert_alpha(), (60, 60)) for r in rutas_caminar]

        # 💥 Secuencia de fotogramas para la explosión
        rutas_muerte = [
            'images/DEATH_1.PNG',
            'images/DEATH_2.PNG'
        ]
        self.sprites_muerte = [pygame.transform.scale(pygame.image.load(r).convert_alpha(), (60, 60)) for r in rutas_muerte]

        # Estado inicial (Empezamos con IDLE)
        self.indice_imagen = 0
        self.image = self.sprites_caminar[self.indice_imagen]
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

        # Variables de control de animación
        self.esta_muriendo = False
        self.ultimo_cambio = pygame.time.get_ticks()
        self.velocidad_animacion = 200  

    def check_edges(self):
        """Devuelve True si el alienígena está en el borde de la pantalla."""
        pantalla_rect = self.pantalla.get_rect()
        if self.rect.right >= pantalla_rect.right or self.rect.left <= 0:
            return True

    def _animar(self):
        """Gestiona las transiciones de fotogramas según el estado actual."""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio > self.velocidad_animacion:
            self.ultimo_cambio = tiempo_actual
            
            if not self.esta_muriendo:
                self.indice_imagen = (self.indice_imagen + 1) % len(self.sprites_caminar)
                self.image = self.sprites_caminar[self.indice_imagen]
            else:
                self.indice_imagen += 1
                if self.indice_imagen < len(self.sprites_muerte):
                    self.image = self.sprites_muerte[self.indice_imagen]
                else:
                    self.kill()

    def update(self):
        """Mueve el alienígena si está vivo y actualiza su animación."""
        if not self.esta_muriendo:
            self.x += (self.ajustes.velocidad_alienigena * self.ajustes.direccion_flota)
            self.rect.x = int(self.x)
        
        self._animar()