# Base weapons class
import pygame


class Weapon:
    
    def __init__(self, owner):
        """
        initialize weapon.
        """
        self.owner = owner
        self.level = 1
        self.enabled = True
        
    def update(self, dt, targets):
        """
        Update weapon logic.
        
        Args:
            dt: Delta time in seconds
            targets: List of potential targets (enemies)
        
        Returns:
            List of projectiles/effects created this frame
        """
        raise NotImplementedError("Subclasses must implement update()")
    
    def draw(self, surface):
        """Draw the weapon (if it has a visual component)."""
        pass
    
    def upgrade(self):
        """Upgrade the weapon to next level."""
        self.level += 1
        self.apply_upgrade()
    
    def apply_upgrade(self):
        """Apply level-specific upgrades. Override in subclasses."""
        pass
    
    def get_info(self):
        """Get weapon information for UI display."""
        return {
            'name': self.__class__.__name__,
            'level': self.level,
            'description': 'Base weapon'
        }