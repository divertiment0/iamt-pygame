import pygame

class Nave:
    """Clase para gestionar la nave del jugador."""

    def __init__(self, ai_juego):
        """Inicializa la nave y establece su posición de salida."""
        self.pantalla = ai_juego.pantalla
        self.pantalla_rect = ai_juego.pantalla.get_rect()
        self.ajustes = ai_juego.ajustes

        # Selector de archivo según tu menú
        if self.ajustes.modelo_nave == 1:
            ruta = 'images/nave_1.png'
        elif self.ajustes.modelo_nave == 2:
            ruta = 'images/nave_2.png'
        elif self.ajustes.modelo_nave == 3:
            ruta = 'images/nave_3.png'
        else:
            ruta = 'images/nave_1.png'

        # 1. Cargamos la imagen original (sea de 256 o 512 píxeles)
        imagen_original = pygame.image.load(ruta).convert_alpha()
        
        # 2. La adaptamos a un tamaño jugable de 80x80 píxeles
        self.image = pygame.transform.scale(imagen_original, (80, 80))

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pantalla_rect.midbottom
        self.x = float(self.rect.x)

        # Banderas de movimiento
        self.movimiento_derecha = False
        self.movimiento_izquierda = False

        # 🎯 EFECTO: Bandera para saber si la nave está dañada
        self.recibiendo_daño = False

    def update(self):
        """Actualiza la posición de la nave respetando los límites de la pantalla."""
        if self.movimiento_derecha:
            self.x += self.ajustes.velocidad_nave
        if self.movimiento_izquierda:
            self.x -= self.ajustes.velocidad_nave

        max_x = self.pantalla_rect.right - self.rect.width
        self.x = max(0, min(self.x, max_x))
        self.rect.x = int(self.x)

    def blitme(self):
        """Dibuja la nave en su posición actual (aplica tinte rojo si recibe daño)."""
        if self.recibiendo_daño:
            # Creamos un filtro translúcido rojo del tamaño de la nave
            superficie_daño = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            superficie_daño.fill((255, 0, 0, 180)) # Rojo con transparencia
            
            # Dibujamos la nave y combinamos el color rojo encima
            self.pantalla.blit(self.image, self.rect)
            self.pantalla.blit(superficie_daño, self.rect, special_flags=pygame.BLEND_RGBA_MULT)
        else:
            # Dibujado normal
            self.pantalla.blit(self.image, self.rect)
