"""
Experience gem - drops from zombies and grants XP when collected
"""
import pygame
import math
from config import *


class ExpGem:
    """An experience gem that the player collects."""
    
    def __init__(self, x, y, value=EXP_BASE_VALUE):
        self.x = x
        self.y = y
        self.value = value
        self.size = 8
        self.color = COLOR_EXP
        
        # Movement toward player when in range
        self.attracted = False
        self.vx = 0
        self.vy = 0
        self.attraction_speed = 400
        
        # Visual effect
        self.pulse = 0
    
    def update(self, dt, player_pos, player_pickup_radius):
        """Update gem position and check if it should move to player."""
        self.pulse += dt * 5  # for pulsing effect
        
        # Check if player is in pickup range
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        distance = math.hypot(dx, dy)
        
        if distance < player_pickup_radius:
            self.attracted = True
        
        # Move toward player if attracted
        if self.attracted and distance > 5:
            # Normalize direction
            if distance > 0:
                self.vx = (dx / distance) * self.attraction_speed
                self.vy = (dy / distance) * self.attraction_speed
                
                self.x += self.vx * dt
                self.y += self.vy * dt
        
        # Return True if player collected it (within 10 pixels)
        return distance < 10
    
    def draw(self, surface):
        """Draw the experience gem with pulsing effect."""
        # Pulsing size
        pulse_size = self.size + int(math.sin(self.pulse) * 2)
        
        # Outer glow
        glow_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(surface, glow_color, 
                          (int(self.x), int(self.y)), pulse_size + 2)
        
        # Inner gem
        pygame.draw.circle(surface, self.color, 
                          (int(self.x), int(self.y)), pulse_size)