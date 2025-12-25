"""
Zombie entity - enemies that chase the player
"""
import pygame
import math
import random
from config import *


class Zombie:
    """A zombie enemy that chases the player."""
    
    def __init__(self, x, y, zombie_type="basic"):
        self.rect = pygame.Rect(0, 0, ZOMBIE_SIZE, ZOMBIE_SIZE)
        self.rect.center = (x, y)
        self.type = zombie_type
        
        # Set stats based on type
        if zombie_type == "basic":
            self.max_health = ZOMBIE_BASE_HEALTH
            self.speed = ZOMBIE_SPEED
            self.color = (50, 150, 50)
            self.exp_value = EXP_BASE_VALUE
            self.damage = 10
        elif zombie_type == "fast":
            self.max_health = ZOMBIE_BASE_HEALTH // 2
            self.speed = ZOMBIE_SPEED * 1.8
            self.color = (150, 150, 50)
            self.exp_value = EXP_BASE_VALUE * 1.5
            self.damage = 8
        elif zombie_type == "tank":
            self.max_health = ZOMBIE_BASE_HEALTH * 3
            self.speed = ZOMBIE_SPEED * 0.6
            self.color = (150, 50, 50)
            self.exp_value = EXP_BASE_VALUE * 3
            self.damage = 20
        
        self.health = self.max_health
        self.alive = True
        
        # Velocity for smooth movement
        self.vx = 0
        self.vy = 0
    
    def update(self, dt, player_pos):
        """Move toward the player."""
        if not self.alive:
            return
        
        # Calculate direction to player
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        
        if distance > 0:
            # Normalize and apply speed
            self.vx = (dx / distance) * self.speed
            self.vy = (dy / distance) * self.speed
            
            # Move
            self.rect.x += self.vx * dt
            self.rect.y += self.vy * dt
    
    def take_damage(self, amount):
        """Reduce health and check for death."""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            return True  # zombie died
        return False
    
    def draw(self, surface):
        """Draw the zombie."""
        if not self.alive:
            return
        
        pygame.draw.rect(surface, self.color, self.rect)
        
        # Draw health bar for damaged zombies
        if self.health < self.max_health:
            bar_width = ZOMBIE_SIZE
            bar_height = 3
            bar_x = self.rect.x
            bar_y = self.rect.y - 8
            
            # Background (dark red)
            pygame.draw.rect(surface, (60, 0, 0), 
                            (bar_x, bar_y, bar_width, bar_height))
            
            # Health (red)
            health_width = int(bar_width * (self.health / self.max_health))
            pygame.draw.rect(surface, (255, 0, 0), 
                            (bar_x, bar_y, health_width, bar_height))