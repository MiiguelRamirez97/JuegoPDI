import pygame
import sys
import random

# Inicializa Pygame
pygame.init()

# Constantes
SCREEN_SIZE = (700, 500)
BIRD_SIZE = (50, 50)
PIPE_WIDTH = 80
GRAVITY = 8
BIRD_JUMP = -35
PIPE_SPEED = -5
PIPE_GAP = 100
PIPE_FREQUENCY = 100
WAIT_TIME = 100

# Crea una fuente
font = pygame.font.Font(None, 36)

# Configura la ventana de juego
screen = pygame.display.set_mode(SCREEN_SIZE)

# Configura el pájaro
bird = pygame.Rect(100, 250, *BIRD_SIZE)

# Inicializa el contador de puntuación
score = 0

# Define una función para generar tuberías
def generate_pipe():
    height = random.randint(100, 300)  # Limita la altura máxima de la tubería
    return [pygame.Rect(700, 0, PIPE_WIDTH, height), pygame.Rect(700, height + PIPE_GAP, PIPE_WIDTH, 500 - height - PIPE_GAP)]

# Inicializa las tuberías
pipes = generate_pipe()

# Define una función para manejar la entrada del usuario
def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            bird.move_ip(0, BIRD_JUMP)

# Define una función para mover las tuberías
def move_pipes():
    global score
    for pipe in pipes:
        pipe.move_ip(PIPE_SPEED, 0)
        if pipe.right == bird.left:  # El pájaro ha pasado la tubería
            score += 0.5

# Define una función para detectar colisiones
def detect_collision():
    for pipe in pipes:
        if bird.colliderect(pipe) or bird.bottom > 500:  # Detecta la colisión
            # Crea una superficie con el texto "Game Over"
            text = font.render("Game Over", True, (255, 255, 255))
            # Dibuja la superficie en la pantalla
            screen.blit(text, (250, 250))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

# Bucle de juego
counter = 1
while True:
    handle_input()
    bird.move_ip(0, GRAVITY)
    move_pipes()
    detect_collision()

    if counter % PIPE_FREQUENCY == 0:  # Genera nuevas tuberías cada 100 iteraciones
        pipes.extend(generate_pipe())
    pipes = [pipe for pipe in pipes if pipe.right > 0]  # Elimina las tuberías que ya no están en la pantalla

    # Dibuja todo
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), bird)
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 255, 0), pipe)

    # Dibuja la puntuación
    text = font.render(str(int(score)), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Actualiza la pantalla
    pygame.display.flip()

    # Espera un poco antes de la próxima iteración
    pygame.time.wait(WAIT_TIME)

    counter += 1