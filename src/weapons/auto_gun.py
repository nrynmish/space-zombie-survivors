"""
Auto Gun - Automatically shoots at the nearest enemy
"""
import math
from weapons.weapon_base import Weapon
from entities.bullet import Bullet
from config import *


class AutoGun(Weapon):
    """Automatically shoots bullets at the nearest enemy."""
    
    def __init__(self, owner):
        super().__init__(owner)
        
        # Weapon stats
        self.fire_rate = 3.0  # Shots per second
        self.damage = BULLET_DAMAGE
        self.bullet_count = 1  # How many bullets per shot
        self.pierce = 0  # How many enemies bullet can pierce
        
        # Internal state
        self.shoot_timer = 0
        self.shoot_cooldown = 1.0 / self.fire_rate
    
    def update(self, dt, targets):
        """Update shooting logic."""
        self.shoot_timer += dt
        
        # Check if we can shoot
        if self.shoot_timer >= self.shoot_cooldown and len(targets) > 0:
            bullets = self.shoot_at_nearest(targets)
            self.shoot_timer = 0
            return bullets
        
        return []
    
    def shoot_at_nearest(self, targets):
        """Find nearest target and shoot at it."""
        # Find nearest alive target
        nearest = None
        min_dist = float('inf')
        
        for target in targets:
            if not target.alive:
                continue
            
            dx = target.rect.centerx - self.owner.rect.centerx
            dy = target.rect.centery - self.owner.rect.centery
            dist = dx * dx + dy * dy
            
            if dist < min_dist:
                min_dist = dist
                nearest = target
        
        if not nearest:
            return []
        
        # Create bullets
        bullets = []
        
        if self.bullet_count == 1:
            # Single bullet
            bullet = Bullet(
                self.owner.rect.centerx,
                self.owner.rect.centery,
                nearest.rect.centerx,
                nearest.rect.centery,
                damage=self.damage
            )
            bullets.append(bullet)
        else:
            # Multiple bullets in a spread
            angle_to_target = math.atan2(
                nearest.rect.centery - self.owner.rect.centery,
                nearest.rect.centerx - self.owner.rect.centerx
            )
            
            spread = math.radians(15)  # 15 degree spread
            angle_step = spread / max(1, self.bullet_count - 1)
            start_angle = angle_to_target - spread / 2
            
            for i in range(self.bullet_count):
                angle = start_angle + (i * angle_step)
                
                # Calculate target point based on angle
                distance = 500  # Shoot distance
                target_x = self.owner.rect.centerx + math.cos(angle) * distance
                target_y = self.owner.rect.centery + math.sin(angle) * distance
                
                bullet = Bullet(
                    self.owner.rect.centerx,
                    self.owner.rect.centery,
                    target_x,
                    target_y,
                    damage=self.damage
                )
                bullets.append(bullet)
        
        return bullets
    
    def apply_upgrade(self):
        """Apply upgrades based on level."""
        if self.level == 2:
            self.fire_rate = 4.0  # Faster shooting
        elif self.level == 3:
            self.bullet_count = 2  # Double shot
        elif self.level == 4:
            self.fire_rate = 5.0  # Even faster
        elif self.level == 5:
            self.bullet_count = 3  # Triple shot
        elif self.level == 6:
            self.damage = BULLET_DAMAGE * 1.5  # More damage
        elif self.level >= 7:
            self.fire_rate = 6.0  # Max fire rate
        
        # Update cooldown based on fire rate
        self.shoot_cooldown = 1.0 / self.fire_rate
    
    def get_info(self):
        """Get weapon information."""
        return {
            'name': 'Auto Gun',
            'level': self.level,
            'description': f'Shoots {self.bullet_count} bullet(s) at {self.fire_rate:.1f}/sec',
            'fire_rate': self.fire_rate,
            'bullet_count': self.bullet_count,
            'damage': self.damage
        }