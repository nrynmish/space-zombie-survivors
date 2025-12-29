"""
Player entity - the character controlled by the user
"""
import pygame
import math
import os
from config import *
from animated_sprite import AnimatedSprite


class Player:
    """The player character controlled by the user."""
    
    def __init__(self, pos):
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.rect.center = pos
        self.color = COLOR_PLAYER
        
        # Stats
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.speed = PLAYER_SPEED
        self.pickup_radius = PLAYER_PICKUP_RADIUS
        
        # State
        self.alive = True
        self.invulnerable_time = 0  # for damage immunity after hit
        
        # Animation
        sprite_path = os.path.join('assets', 'sprites', 'player_idle.png')
        self.animation = AnimatedSprite(
            sprite_sheet_path=sprite_path,
            frame_width=64,
            frame_height=64,
            num_frames=3,
            fps=6,
            layout='vertical'
        )
        
    def handle_input(self, keys, dt):
        """Handle WASD/Arrow key movement."""
        if not self.alive:
            return
            
        vx = 0
        vy = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vy += 1

        # Normalize diagonal movement
        if vx != 0 or vy != 0:
            mag = math.hypot(vx, vy)
            vx /= mag
            vy /= mag
            self.rect.x += int(vx * self.speed * dt)
            self.rect.y += int(vy * self.speed * dt)
    
    def clamp(self, width, height):
        """Keep player within screen bounds."""
        self.rect.clamp_ip(pygame.Rect(0, 0, width, height))
    
    def take_damage(self, amount):
        """Reduce health and check for death."""
        if self.invulnerable_time > 0:
            return False
            
        self.health -= amount
        self.invulnerable_time = 0.5  # 0.5 seconds of immunity
        
        if self.health <= 0:
            self.health = 0
            self.alive = False
            return True  # player died
        return False
    
    def update(self, dt):
        """Update player state."""
        if self.invulnerable_time > 0:
            self.invulnerable_time -= dt
        
        # Update animation
        self.animation.update(dt)
    
    def draw(self, surface):
        """Draw the player."""
        # Flash when invulnerable
        if self.invulnerable_time > 0 and int(self.invulnerable_time * 10) % 2:
            return  # Skip drawing to create flash effect
        
        # Draw animated sprite
        current_frame = self.animation.get_current_frame()
        
        # Center the 64x64 sprite on the 32x32 collision rect
        sprite_rect = current_frame.get_rect()
        sprite_rect.center = self.rect.center
        surface.blit(current_frame, sprite_rect)
        
        # Draw health bar above player
        bar_width = 64  # Match sprite width
        bar_height = 4
        bar_x = sprite_rect.x
        bar_y = sprite_rect.y - 10
        
        # Background (red)
        pygame.draw.rect(surface, (100, 0, 0), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(surface, (0, 255, 0), 
                        (bar_x, bar_y, health_width, bar_height))