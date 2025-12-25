"""
Bullet projectile - fired by player weapons
"""
import pygame
import math
from config import *


class Bullet:
    """A projectile fired by weapons."""
    
    def __init__(self, start_x, start_y, target_x, target_y, damage=BULLET_DAMAGE):
        self.x = start_x
        self.y = start_y
        self.damage = damage
        self.radius = 5
        self.color = COLOR_BULLET
        
        # Calculate direction
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.hypot(dx, dy)
        
        if distance > 0:
            self.vx = (dx / distance) * BULLET_SPEED
            self.vy = (dy / distance) * BULLET_SPEED
        else:
            self.vx = 0
            self.vy = 0
        
        self.alive = True
        self.pierce_count = 0  # how many enemies it can pierce through
    
    def update(self, dt, screen_width, screen_height):
        """Move the bullet and check if it's off screen."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Check if off screen
        margin = 50
        if (self.x < -margin or self.x > screen_width + margin or
            self.y < -margin or self.y > screen_height + margin):
            self.alive = False
        
        return self.alive
    
    def check_collision(self, zombie):
        """Check if bullet hit a zombie."""
        if not self.alive or not zombie.alive:
            return False
        
        # Simple circle-rect collision
        closest_x = max(zombie.rect.left, min(self.x, zombie.rect.right))
        closest_y = max(zombie.rect.top, min(self.y, zombie.rect.bottom))
        
        distance = math.hypot(self.x - closest_x, self.y - closest_y)
        
        if distance < self.radius:
            zombie.take_damage(self.damage)
            self.pierce_count += 1
            
            # Bullet dies unless it can pierce
            if self.pierce_count >= 1:  # change this for pierce upgrades
                self.alive = False
            
            return True
        
        return False
    
    def draw(self, surface):
        """Draw the bullet."""
        if self.alive:
            # Glow effect
            pygame.draw.circle(surface, (255, 255, 150), 
                             (int(self.x), int(self.y)), self.radius + 2)
            pygame.draw.circle(surface, self.color, 
                             (int(self.x), int(self.y)), self.radius)