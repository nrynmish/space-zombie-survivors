"""
Zombie spawner system - manages spawning of zombie waves
"""
import pygame
import random
from entities.zombie import Zombie
from config import *


class ZombieSpawner:
    """Manages spawning zombies at screen edges."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_timer = 0
        self.spawn_rate = ZOMBIE_SPAWN_RATE  # seconds between spawns
        
        # Difficulty scaling
        self.game_time = 0
        self.zombies_spawned = 0
        
        # Spawn edges (top, right, bottom, left)
        self.spawn_margin = 50
    
    def update(self, dt):
        """Update spawn timer and increase difficulty over time."""
        self.game_time += dt
        self.spawn_timer += dt
        
        # Increase difficulty every 30 seconds
        difficulty_multiplier = 1 + (self.game_time // 30) * 0.2
        adjusted_spawn_rate = ZOMBIE_SPAWN_RATE / difficulty_multiplier
        
        return adjusted_spawn_rate
    
    def should_spawn(self, dt):
        """Check if it's time to spawn a zombie."""
        adjusted_rate = self.update(dt)
        
        if self.spawn_timer >= adjusted_rate:
            self.spawn_timer = 0
            return True
        return False
    
    def spawn_zombie(self):
        """Spawn a zombie at a random edge position."""
        # Choose random edge
        edge = random.choice(['top', 'right', 'bottom', 'left'])
        
        if edge == 'top':
            x = random.randint(0, self.screen_width)
            y = -self.spawn_margin
        elif edge == 'right':
            x = self.screen_width + self.spawn_margin
            y = random.randint(0, self.screen_height)
        elif edge == 'bottom':
            x = random.randint(0, self.screen_width)
            y = self.screen_height + self.spawn_margin
        else:  # left
            x = -self.spawn_margin
            y = random.randint(0, self.screen_height)
        
        # Determine zombie type based on game time
        zombie_type = self.choose_zombie_type()
        
        self.zombies_spawned += 1
        return Zombie(x, y, zombie_type)
    
    def choose_zombie_type(self):
        """Choose zombie type based on difficulty."""
        # Early game: only basic zombies
        if self.game_time < 30:
            return "basic"
        
        # Mid game: introduce fast zombies
        if self.game_time < 60:
            return random.choices(
                ["basic", "fast"],
                weights=[0.7, 0.3]
            )[0]
        
        # Late game: all types
        return random.choices(
            ["basic", "fast", "tank"],
            weights=[0.5, 0.3, 0.2]
        )[0]
    
    def spawn_batch(self, count):
        """Spawn multiple zombies at once."""
        zombies = []
        for _ in range(count):
            zombies.append(self.spawn_zombie())
        return zombies