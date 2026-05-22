class Ajustes:
    """Clase para guardar todos los ajustes estáticos y dinámicos del juego."""

    def __init__(self):
        """Inicializa los ajustes estáticos del juego."""
        # Ajustes de la pantalla
        self.ancho_pantalla = 1200
        self.alto_pantalla = 800
        self.color_fondo = (230, 230, 230) # Gris claro

        # Ajustes de la nave
        self.velocidad_nave = 4.0  # Un pelín más rápido para compensar el peligro
        self.modelo_nave = 1
        self.limite_naves = 3  

        # Ajustes de los láseres
        self.velocidad_bala = 5.0
        self.ancho_bala = 4
        self.alto_bala = 18
        self.color_bala = (255, 0, 0)
        self.balas_permitidas = 3  

        # Ajustes de dificultad
        self.escala_incremento = 1.2  
        self.inicializar_ajustes_dinamicos()

    def inicializar_ajustes_dinamicos(self):
        """Inicializa los ajustes que cambian a lo largo del juego."""
        self.velocidad_alienigena = 0.5     
        self.velocidad_caida_flota = 15     # <--- 🛠️ ¡Subido de 4 a 15! Ahora bajan con ganas
        self.direccion_flota = 1            

    def aumentar_velocidad(self):
        """Aumenta los ajustes de velocidad al pasar de nivel."""
        self.velocidad_alienigena *= self.escala_incremento
        self.velocidad_caida_flota *= self.escala_incremento
        print(f"📈 ¡NIVEL COMPLETADO! Nueva velocidad lateral: {self.velocidad_alienigena:.2f}")