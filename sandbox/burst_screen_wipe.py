import pygame
import random
import math

class ScreenWipeBurst:
    def __init__(self, screen_width, screen_height, num_particles=50, particle_speed=5, max_size=100):
        """
        Initialize the burst animation.

        Args:
            screen_width (int): Width of the screen.
            screen_height (int): Height of the screen.
            num_particles (int): Number of particles in the burst.
            particle_speed (int): Speed of particle expansion.
            max_size (int): Maximum size of each particle before it stops growing.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_particles = num_particles
        self.particle_speed = particle_speed
        self.max_size = max_size
        self.particles = []

        # Initialize particles at the center of the screen
        for _ in range(self.num_particles):
            angle = random.uniform(0, 2 * math.pi)  # Random direction
            self.particles.append({
                "x": screen_width // 2,
                "y": screen_height // 2,
                "vx": math.cos(angle) * particle_speed,
                "vy": math.sin(angle) * particle_speed,
                "size": 0  # Initial size
            })

        self.animation_complete = False

    def update(self):
        """
        Update the position and size of each particle.
        """
        if self.animation_complete:
            return

        for particle in self.particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["size"] += self.particle_speed / 2

        # Check if all particles have reached the max size
        if all(p["size"] >= self.max_size for p in self.particles):
            self.animation_complete = True

    def draw(self, screen):
        """
        Draw the burst particles on the screen.

        Args:
            screen (pygame.Surface): The screen to draw the particles on.
        """
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 255, 255), (int(particle["x"]), int(particle["y"])), int(particle["size"]))

    def is_complete(self):
        """
        Check if the animation is complete.

        Returns:
            bool: True if the animation is complete, False otherwise.
        """
        return self.animation_complete


import pygame

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Burst Screen Wipe Animation")
BLACK = (0, 0, 0)

# Initialize the burst animation
burst_animation = ScreenWipeBurst(SCREEN_WIDTH, SCREEN_HEIGHT, num_particles=100, particle_speed=10, max_size=200)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Update and draw the burst animation
    burst_animation.update()
    burst_animation.draw(screen)

    # Stop animation when complete
    if burst_animation.is_complete():
        print("Animation complete!")
        running = False

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
