import pygame

def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No gamepad detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    name = joystick.get_name()

    print(f"Detected gamepad: {name}")
    print(f"Axes: {joystick.get_numaxes()}")
    print(f"Buttons: {joystick.get_numbuttons()}")
    print(f"Hats: {joystick.get_numhats()}")
    print("Press buttons or move the D-pad / axes...")

    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Gamepad Test")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button down: {event.button}")

            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button up: {event.button}")

            elif event.type == pygame.JOYHATMOTION:
                print(f"Hat {event.hat}: {event.value}")

            elif event.type == pygame.JOYAXISMOTION:
                # Ignore tiny jitter around center
                if abs(event.value) > 0.2:
                    print(f"Axis {event.axis}: {event.value:.3f}")

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()