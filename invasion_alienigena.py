import sys
import pygame
from time import sleep
from ajustes import Ajustes
from nave import Nave
from alienigena import Alienigena
from bala import Bala 

class InvasionAlienigena:
    """Clase general para gestionar los recursos y el comportamiento del juego."""

    def __init__(self):
        """Inicializa el juego, pide la nave por consola y crea los recursos."""
        pygame.init()
        pygame.joystick.init()

        self.ajustes = Ajustes()

        # 💻 MENÚ INTERACTIVO POR CONSOLA
        self._seleccionar_nave_consola()

        self.pantalla = pygame.display.set_mode(
            (self.ajustes.ancho_pantalla, self.ajustes.alto_pantalla)
        )
        pygame.display.set_caption("Invasión Alienígena")
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.vidas_restantes = self.ajustes.limite_naves
        self.juego_activo = True
        self.nivel = 1  

        # Gamepad
        self.joystick = None
        self._inicializar_gamepad()

        # Instanciamos la nave y grupos con el modelo seleccionado cargado
        self.nave = Nave(self)
        self.balas = pygame.sprite.Group()
        self.alienigenas = pygame.sprite.Group()

        self._crear_flota()

    def _inicializar_gamepad(self):
        """Detecta e inicializa el primer gamepad disponible."""
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"🎮 Gamepad detectado: {self.joystick.get_name()}")
        else:
            print("🎮 No se detectó ningún gamepad. Se usará teclado.")

    def _seleccionar_nave_consola(self):
        """Muestra el menú de selección en la terminal antes de abrir la ventana."""
        print("\n=======================================")
        print("🚀 BIENVENIDO A INVASIÓN ALIENÍGENA 🚀")
        print("=======================================")
        print("Selecciona tu modelo de nave para la batalla:")
        print("1. Nave Clásica")
        print("2. Caza Interceptor")
        print("3. Acorazado Pesado")
        print("=======================================")
        
        while True:
            eleccion = input("Introduce el número de tu nave (1-3): ").strip()
            if eleccion in ['1', '2', '3']:
                self.ajustes.modelo_nave = int(eleccion)
                print(f"\n¡Sistemas listos! Modelo {eleccion} desplegado. ¡A la batalla!\n")
                break
            else:
                print("❌ Entrada no válida. Por favor, introduce 1, 2 o 3.")

    def run_game(self):
        """Inicia el bucle principal para el juego."""
        while True:
            self._revisar_eventos()
            
            if self.juego_activo:
                self.nave.update()
                self._actualizar_balas()
                self._actualizar_alienigenas()

            self._actualizar_pantalla()

    def _revisar_eventos(self):
        """Responde a teclado, gamepad y cierre de ventana."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._revisar_eventos_keydown(event)

            elif event.type == pygame.KEYUP:
                self._revisar_eventos_keyup(event)

            elif event.type == pygame.JOYHATMOTION:
                self._revisar_hat_gamepad(event)

            elif event.type == pygame.JOYAXISMOTION:
                self._revisar_axis_gamepad(event)

            elif event.type == pygame.JOYBUTTONDOWN:
                self._revisar_boton_gamepad(event)

    def _revisar_eventos_keydown(self, event):
        """Responde a las pulsaciones de teclas."""
        if event.key == pygame.K_RIGHT:
            self.nave.movimiento_derecha = True
        elif event.key == pygame.K_LEFT:
            self.nave.movimiento_izquierda = True
        elif event.key == pygame.K_SPACE:
            self._disparar_bala()
        elif event.key == pygame.K_ESCAPE:
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)
            pygame.quit()
            sys.exit()

    def _revisar_eventos_keyup(self, event):
        """Responde a las liberaciones de teclas."""
        if event.key == pygame.K_RIGHT:
            self.nave.movimiento_derecha = False
        elif event.key == pygame.K_LEFT:
            self.nave.movimiento_izquierda = False

    def _revisar_hat_gamepad(self, event):
        """Movimiento con cruceta/D-pad."""
        x, y = event.value

        self.nave.movimiento_izquierda = (x == -1)
        self.nave.movimiento_derecha = (x == 1)

    def _revisar_axis_gamepad(self, event):
        """Movimiento con stick analógico, si existe."""
        if event.axis == 0:
            if event.value < -0.3:
                self.nave.movimiento_izquierda = True
                self.nave.movimiento_derecha = False
            elif event.value > 0.3:
                self.nave.movimiento_derecha = True
                self.nave.movimiento_izquierda = False
            else:
                self.nave.movimiento_izquierda = False
                self.nave.movimiento_derecha = False

    def _revisar_boton_gamepad(self, event):
        """Disparo con botones del gamepad."""
        if event.button in (0, 1, 2, 3):
            self._disparar_bala()

    def _disparar_bala(self):
        """Crea un láser nuevo si no se supera el límite."""
        if self.juego_activo:
            if len(self.balas) < self.ajustes.balas_permitidas:
                nueva_bala = Bala(self)
                self.balas.add(nueva_bala)

    def _actualizar_balas(self):
        """Actualiza la posición de las balas y gestiona las colisiones."""
        self.balas.update()

        for bala in self.balas.copy():
            if bala.rect.bottom <= 0:
                self.balas.remove(bala)

        self._revisar_colisiones_bala_alien()

    def _revisar_colisiones_bala_alien(self):
        """Responde a las colisiones entre balas y alienígenas."""
        colisiones = pygame.sprite.groupcollide(self.balas, self.alienigenas, True, False)

        for aliens_golpeados in colisiones.values():
            for alien in aliens_golpeados:
                if hasattr(alien, 'esta_muriendo'):
                    if not alien.esta_muriendo:
                        alien.esta_muriendo = True
                        alien.indice_imagen = 0
                        if hasattr(alien, 'sprites_muerte'):
                            alien.image = alien.sprites_muerte[0]
                else:
                    alien.kill()

        if self.alienigenas.sprites() and hasattr(self.alienigenas.sprites()[0], 'esta_muriendo'):
            aliens_vivos = [a for a in self.alienigenas.sprites() if not a.esta_muriendo]
            explotando = any(a.esta_muriendo for a in self.alienigenas.sprites())
        else:
            aliens_vivos = self.alienigenas.sprites()
            explotando = False

        if not aliens_vivos and not explotando:
            self.balas.empty()
            self.ajustes.aumentar_velocidad()  
            self.nivel += 1
            print(f"🌌 ¡PREPÁRATE! Iniciando Oleada número {self.nivel}")
            self._crear_flota()

    def _actualizar_alienigenas(self):
        """Comprueba si la flota está en un borde y actualiza las posiciones."""
        self._check_flota_edges()
        self.alienigenas.update()

        if self.alienigenas.sprites() and hasattr(self.alienigenas.sprites()[0], 'esta_muriendo'):
            aliens_vivos = [a for a in self.alienigenas.sprites() if not a.esta_muriendo]
        else:
            aliens_vivos = self.alienigenas.sprites()

        for alien in aliens_vivos:
            if alien.rect.colliderect(self.nave.rect):
                self._nave_golpeada()
                break

        self._check_alienigenas_fondo()

    def _nave_golpeada(self):
        """Responde al impacto de un alienígena contra la nave."""
        if self.vidas_restantes > 1:
            self.vidas_restantes -= 1
            print(f"💥 ¡Impacto crítico! Vidas restantes: {self.vidas_restantes}")
            
            self.nave.recibiendo_daño = True
            self._actualizar_pantalla()
            sleep(0.3)
            
            self.nave.recibiendo_daño = False
            
            self.alienigenas.empty()
            self.balas.empty()
            self._crear_flota()
            
            pantalla_rect = self.pantalla.get_rect()
            self.nave.rect.midbottom = pantalla_rect.midbottom
            self.nave.x = float(self.nave.rect.x)
            sleep(0.5)
        else:
            self.juego_activo = False
            print(f"\n💀 GAME OVER 💀 Llegaste hasta la Oleada {self.nivel}.")

    def _check_alienigenas_fondo(self):
        """Comprueba si algún alienígena vivo ha alcanzado el fondo."""
        pantalla_rect = self.pantalla.get_rect()
        
        if self.alienigenas.sprites() and hasattr(self.alienigenas.sprites()[0], 'esta_muriendo'):
            aliens_vivos = [a for a in self.alienigenas.sprites() if not a.esta_muriendo]
        else:
            aliens_vivos = self.alienigenas.sprites()

        for alien in aliens_vivos:
            if alien.rect.bottom >= pantalla_rect.bottom:
                self._nave_golpeada()
                break

    def _check_flota_edges(self):
        """Actúa si algún alienígena vivo alcanza un borde."""
        if self.alienigenas.sprites() and hasattr(self.alienigenas.sprites()[0], 'esta_muriendo'):
            aliens_vivos = [a for a in self.alienigenas.sprites() if not a.esta_muriendo]
        else:
            aliens_vivos = self.alienigenas.sprites()

        for alien in aliens_vivos:
            if alien.check_edges():
                self._cambiar_direccion_flota()
                break

    def _cambiar_direccion_flota(self):
        """Baja toda la flota rápidamente y cambia su dirección lateral."""
        for alienigena in self.alienigenas.sprites():
            alienigena.rect.y += self.ajustes.velocidad_caida_flota
        self.ajustes.direccion_flota *= -1

    def _crear_flota(self):
        """Crea la flota de alienígenas."""
        alienigena_aux = Alienigena(self)
        ancho_alien, alto_alien = alienigena_aux.rect.size

        limite_coordenada_x = self.ajustes.ancho_pantalla - (2 * ancho_alien)
        limite_coordenada_y = self.ajustes.alto_pantalla - self.nave.rect.height - (4 * alto_alien)

        puntero_y = alto_alien

        while puntero_y < limite_coordenada_y:
            puntero_x = ancho_alien
            while puntero_x < limite_coordenada_x:
                self._inicializar_alienigena_en_coordenada(puntero_x, puntero_y)
                puntero_x += 2 * ancho_alien
            puntero_y += 2 * alto_alien

    def _inicializar_alienigena_en_coordenada(self, coordenada_x, coordenada_y):
        """Instancia y ubica un alienígena."""
        nuevo_alienigena = Alienigena(self)
        nuevo_alienigena.x = float(coordenada_x)
        nuevo_alienigena.rect.x = coordenada_x
        nuevo_alienigena.rect.y = coordenada_y
        self.alienigenas.add(nuevo_alienigena)

    def _actualizar_pantalla(self):
        """Actualiza las imágenes en la pantalla."""
        self.pantalla.fill(self.ajustes.color_fondo)
        
        for bala in self.balas.sprites():
            bala.draw_bullet()

        self.nave.blitme()
        self.alienigenas.draw(self.pantalla)
        pygame.display.flip()

if __name__ == '__main__':
    try:
        ai = InvasionAlienigena()
        ai.run_game()
    except KeyboardInterrupt:
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
        print("\n[INFO] Juego cerrado correctamente. ¡Hasta la próxima!")
        sys.exit()
