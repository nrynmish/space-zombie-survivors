"""
Experience system - manages player XP and leveling
"""
from config import *


class ExperienceSystem:
    """Manages player experience and level ups."""
    
    def __init__(self):
        self.level = 1
        self.current_exp = 0
        self.exp_to_next_level = EXP_TO_LEVEL
        self.total_exp = 0
        
    def add_exp(self, amount):
        """Add experience and check for level up."""
        self.current_exp += amount
        self.total_exp += amount
        
        # Check if leveled up
        if self.current_exp >= self.exp_to_next_level:
            return self.level_up()
        
        return False
    
    def level_up(self):
        """Increase level and reset exp bar."""
        self.current_exp -= self.exp_to_next_level
        self.level += 1
        
        # Increase exp requirement for next level
        self.exp_to_next_level = int(self.exp_to_next_level * EXP_LEVEL_MULTIPLIER)
        
        return True  # Signal that player leveled up
    
    def get_progress(self):
        """Get current exp progress as a percentage (0.0 to 1.0)."""
        return self.current_exp / self.exp_to_next_level
    
    def get_level_info(self):
        """Get formatted level information."""
        return {
            'level': self.level,
            'current_exp': self.current_exp,
            'exp_to_next': self.exp_to_next_level,
            'progress': self.get_progress(),
            'total_exp': self.total_exp
        }