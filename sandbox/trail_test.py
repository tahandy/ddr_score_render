import pygame
from score_render.elements import ParticleTrail  # Assuming the class is saved in `particle_trail.py`

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle Trail Effect")
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Object settings
object_width = 20
object_height = 20
object_x = SCREEN_WIDTH // 2
object_y = SCREEN_HEIGHT // 2
object_speed = 5

# Particle trail
particle_trail = ParticleTrail(color=(0, 0, 0), max_particles=600, particle_lifetime=60)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Object movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        object_x -= object_speed
    if keys[pygame.K_RIGHT]:
        object_x += object_speed

    # Emit particles at the object's position
    particle_trail.emit(object_x + object_width // 2, object_y + object_height)

    # Update particles
    particle_trail.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the object
    pygame.draw.rect(screen, BLUE, (object_x, object_y, object_width, object_height))

    # Draw the particle trail
    particle_trail.draw(screen)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
