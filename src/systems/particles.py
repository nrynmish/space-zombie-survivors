"""
Void particle system - visual effects for the void theme
"""
import pygame
import random
import math
from config import *


class VoidParticle:
    """A single floating void particle that fades out over time."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-80, 80)
        self.vy = random.uniform(-80, 80)
        self.life = 1.0  # 1.0 = fully visible, 0.0 = invisible
        self.max_life = random.uniform(1.5, 3.0)
        self.size = random.randint(2, 8)
        self.color = (80 + random.randint(-20, 20), 20, 100 + random.randint(-20, 20))
    
    def update(self, dt):
        """Move the particle and fade it out."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt / self.max_life
        return self.life > 0
    
    def draw(self, surface):
        """Draw the particle with fading visibility."""
        alpha = int(255 * self.life)
        color = tuple(min(255, int(c * self.life)) for c in self.color)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class DeathParticle:
    """Particle effect for zombie deaths."""
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(100, 300)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.max_life = random.uniform(0.3, 0.8)
        self.size = random.randint(3, 7)
        self.color = color
        self.gravity = 400  # particles fall down
    
    def update(self, dt):
        """Move with velocity and gravity."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt  # apply gravity
        self.life -= dt / self.max_life
        return self.life > 0
    
    def draw(self, surface):
        """Draw the particle."""
        alpha = int(255 * self.life)
        color = tuple(min(255, int(c * self.life)) for c in self.color)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


def create_death_particles(x, y, color, count=15):
    """Create a burst of particles at a position."""
    return [DeathParticle(x, y, color) for _ in range(count)]


def create_void_particles(x, y, count=5):
    """Create void particles around a position."""
    particles = []
    for _ in range(count):
        offset_x = random.randint(-50, 50)
        offset_y = random.randint(-50, 50)
        particles.append(VoidParticle(x + offset_x, y + offset_y))
    return particles