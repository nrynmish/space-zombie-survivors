"""
Boss Zombie - A powerful mega-zombie with special abilities
"""
import pygame
import math
import random
from entities.zombie import Zombie
from config import *


class BossZombie(Zombie):
    """A massive boss zombie with high health and special attacks."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "basic")  # Initialize as basic zombie first
        
        # Boss stats - MUCH stronger!
        self.max_health = 2000  # Lots of HP!
        self.health = self.max_health
        self.speed = ZOMBIE_SPEED * 0.8  # Slower but menacing
        self.damage = 30  # Hits hard!
        self.exp_value = 500  # Huge XP reward
        
        # Boss appearance
        self.size = 64  # 2x bigger than normal zombies
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (x, y)
        self.color = (200, 50, 200)  # Purple boss color
        
        # Boss special abilities
        self.spawn_timer = 0
        self.spawn_cooldown = 5.0  # Spawn minions every 5 seconds
        
        # Visual effects
        self.pulse = 0
        
    def update(self, dt, player_pos):
        """Update boss with special abilities."""
        super().update(dt, player_pos)
        
        # Pulsing effect
        self.pulse += dt * 3
        
        # Spawn minion timer
        self.spawn_timer += dt
        
    def should_spawn_minion(self):
        """Check if boss should spawn a minion zombie."""
        if self.spawn_timer >= self.spawn_cooldown:
            self.spawn_timer = 0
            return True
        return False
    
    def draw(self, surface):
        """Draw the boss with special effects."""
        if not self.alive:
            return
        
        # Pulsing size effect
        pulse_size = int(math.sin(self.pulse) * 4)
        draw_size = self.size + pulse_size
        
        # Draw glow effect
        glow_rect = pygame.Rect(0, 0, draw_size + 20, draw_size + 20)
        glow_rect.center = self.rect.center
        glow_color = (150, 50, 150, 100)
        pygame.draw.rect(surface, glow_color, glow_rect, border_radius=10)
        
        # Draw main body with pulsing
        draw_rect = pygame.Rect(0, 0, draw_size, draw_size)
        draw_rect.center = self.rect.center
        pygame.draw.rect(surface, self.color, draw_rect)
        
        # Draw eyes (scary!)
        eye_size = 8
        left_eye_x = draw_rect.centerx - 15
        right_eye_x = draw_rect.centerx + 15
        eye_y = draw_rect.centery - 10
        pygame.draw.circle(surface, (255, 0, 0), (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(surface, (255, 0, 0), (right_eye_x, eye_y), eye_size)
        
        # Draw health bar (BIGGER for boss)
        bar_width = self.size + 20
        bar_height = 8
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.y - 20
        
        # Background (dark red)
        pygame.draw.rect(surface, (60, 0, 0), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Health (red to orange gradient based on health)
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        
        if health_ratio > 0.5:
            bar_color = (255, 0, 0)
        elif health_ratio > 0.25:
            bar_color = (255, 100, 0)
        else:
            bar_color = (255, 200, 0)
        
        pygame.draw.rect(surface, bar_color, 
                        (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, (150, 150, 150), 
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # HP text
        font = pygame.font.SysFont(None, 20)
        hp_text = font.render(f"{int(self.health)}/{int(self.max_health)}", True, (255, 255, 255))
        hp_rect = hp_text.get_rect(center=(bar_x + bar_width // 2, bar_y - 12))
        surface.blit(hp_text, hp_rect)