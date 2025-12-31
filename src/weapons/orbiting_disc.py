"""
Orbiting Disc - Rotating blade that orbits around the player
"""
import pygame
import math
from weapons.weapon_base import Weapon
from config import *


class OrbitingDisc(Weapon):
    """A disc that rotates around the player and damages enemies on contact."""
    
    def __init__(self, owner):
        super().__init__(owner)
        
        # Weapon stats
        self.disc_count = 1  # Number of discs
        self.radius = DISC_RADIUS  # Distance from player
        self.rotation_speed = DISC_ROTATION_SPEED  # Degrees per second
        self.damage = DISC_DAMAGE  # Damage per hit
        self.size = 12  # Disc visual size
        
        # Visual
        self.color = (100, 200, 255)  # Cyan color
        
        # Internal state
        self.angle = 0  # Current rotation angle in degrees
        self.hit_cooldown = {}  # Track when we last hit each enemy
        self.hit_delay = 0.5  # Seconds between hits on same enemy
    
    def update(self, dt, targets):
        """Update disc rotation and check for collisions."""
        # Rotate the disc
        self.angle += self.rotation_speed * dt
        self.angle %= 360  # Keep angle between 0-360
        
        # Check collisions with targets
        self.check_collisions(targets, dt)
        
        return []  # Discs don't create projectiles
    
    def get_disc_positions(self):
        """Calculate the position of each disc."""
        positions = []
        
        angle_offset = 360 / self.disc_count  # Evenly space discs around player
        
        for i in range(self.disc_count):
            # Calculate angle for this disc
            disc_angle = self.angle + (i * angle_offset)
            disc_angle_rad = math.radians(disc_angle)
            
            # Calculate position
            x = self.owner.rect.centerx + math.cos(disc_angle_rad) * self.radius
            y = self.owner.rect.centery + math.sin(disc_angle_rad) * self.radius
            
            positions.append((x, y))
        
        return positions
    
    def check_collisions(self, targets, dt):
        """Check if any disc hit any target."""
        disc_positions = self.get_disc_positions()
        
        for target in targets:
            if not target.alive:
                continue
            
            # Check cooldown for this target
            target_id = id(target)
            if target_id in self.hit_cooldown:
                self.hit_cooldown[target_id] -= dt
                if self.hit_cooldown[target_id] > 0:
                    continue  # Still on cooldown
            
            # Check collision with each disc
            for disc_x, disc_y in disc_positions:
                # Simple circle-rect collision
                closest_x = max(target.rect.left, min(disc_x, target.rect.right))
                closest_y = max(target.rect.top, min(disc_y, target.rect.bottom))
                
                distance = math.hypot(disc_x - closest_x, disc_y - closest_y)
                
                if distance < self.size:
                    # Hit!
                    target.take_damage(self.damage)
                    self.hit_cooldown[target_id] = self.hit_delay
                    break  # Only hit once per frame
        
        # Clean up old cooldowns for dead enemies
        self.hit_cooldown = {k: v for k, v in self.hit_cooldown.items() if v > 0}
    
    def draw(self, surface):
        """Draw the rotating discs."""
        disc_positions = self.get_disc_positions()
        
        for disc_x, disc_y in disc_positions:
            # Draw outer glow
            glow_color = tuple(min(255, c + 50) for c in self.color)
            pygame.draw.circle(surface, glow_color, 
                             (int(disc_x), int(disc_y)), self.size + 3)
            
            # Draw main disc
            pygame.draw.circle(surface, self.color, 
                             (int(disc_x), int(disc_y)), self.size)
            
            # Draw inner core (darker)
            core_color = tuple(c // 2 for c in self.color)
            pygame.draw.circle(surface, core_color, 
                             (int(disc_x), int(disc_y)), self.size // 2)
    
    def apply_upgrade(self):
        """Apply upgrades based on level."""
        if self.level == 2:
            self.disc_count = 2  # Add second disc
        elif self.level == 3:
            self.rotation_speed = DISC_ROTATION_SPEED * 1.3  # Faster rotation
        elif self.level == 4:
            self.disc_count = 3  # Add third disc
        elif self.level == 5:
            self.radius = DISC_RADIUS * 1.2  # Larger orbit
        elif self.level == 6:
            self.disc_count = 4  # Add fourth disc
        elif self.level == 7:
            self.damage = DISC_DAMAGE * 1.5  # More damage
        elif self.level >= 8:
            self.size = 16  # Bigger discs
    
    def get_info(self):
        """Get weapon information."""
        return {
            'name': 'Orbiting Disc',
            'level': self.level,
            'description': f'{self.disc_count} disc(s) orbiting at {self.rotation_speed:.0f}°/s',
            'disc_count': self.disc_count,
            'rotation_speed': self.rotation_speed,
            'damage': self.damage,
            'radius': self.radius
        }