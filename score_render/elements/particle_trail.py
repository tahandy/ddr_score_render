import pygame
import random

class ParticleTrail:
    def __init__(self, color, max_particles=100, particle_lifetime=60):
        """
        Initialize the particle trail effect.

        Args:
            color (tuple): RGB color of the particles.
            max_particles (int): Maximum number of particles to retain.
            particle_lifetime (int): Number of frames each particle lasts.
        """
        self.color = color
        self.max_particles = max_particles
        self.particle_lifetime = particle_lifetime
        self.particles = []

    def emit(self, x, y):
        """
        Emit a new particle at the specified position.

        Args:
            x (int): X-coordinate of the particle's starting position.
            y (int): Y-coordinate of the particle's starting position.
        """
        particle = {
            "x": x,
            "y": y,
            "vx": random.uniform(-1, 1),  # Random horizontal drift
            "vy": random.uniform(1, 3),  # Downward velocity
            "life": self.particle_lifetime
        }
        self.particles.append(particle)

        # Limit the number of particles
        if len(self.particles) > self.max_particles:
            self.particles.pop(0)

    def update(self):
        """
        Update particle positions and reduce their lifetime.
        """
        for particle in self.particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1

        # Remove dead particles
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, screen):
        """
        Draw the particles on the screen.

        Args:
            screen (pygame.Surface): Surface to draw the particles on.
        """
        for particle in self.particles:
            alpha = int(255 * (particle["life"] / self.particle_lifetime))  # Fade out effect
            particle_color = (*self.color, alpha)
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)  # Particle size: 4x4
            pygame.draw.circle(particle_surface, particle_color, (2, 2), 2)
            screen.blit(particle_surface, (particle["x"], particle["y"]))
