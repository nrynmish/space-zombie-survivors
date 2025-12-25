"""
HUD - Heads-up display for game information
"""
import pygame
from config import *


class HUD:
    """Displays game information like health, exp, level, time."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont(None, 36)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 24)
    
    def draw(self, surface, player, exp_system, game_time, kills):
        """Draw all HUD elements."""
        # Top-left: Level and kills
        level_text = self.font_large.render(f"Level {exp_system.level}", True, (255, 255, 255))
        surface.blit(level_text, (20, 20))
        
        kills_text = self.font_medium.render(f"Kills: {kills}", True, (200, 200, 200))
        surface.blit(kills_text, (20, 60))
        
        # Top-right: Timer
        minutes = int(game_time // 60)
        seconds = int(game_time % 60)
        time_text = self.font_large.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        time_rect = time_text.get_rect()
        time_rect.topright = (self.screen_width - 20, 20)
        surface.blit(time_text, time_rect)
        
        # Bottom: Experience bar
        self.draw_exp_bar(surface, exp_system)
        
        # Top-center: Health bar
        self.draw_health_bar(surface, player)
    
    def draw_exp_bar(self, surface, exp_system):
        """Draw the experience progress bar at the bottom."""
        bar_height = 20
        bar_y = self.screen_height - bar_height - 10
        bar_x = 20
        bar_width = self.screen_width - 40
        
        # Background
        pygame.draw.rect(surface, (30, 30, 50), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Progress fill
        progress = exp_system.get_progress()
        fill_width = int(bar_width * progress)
        pygame.draw.rect(surface, (100, 200, 255), 
                        (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, (100, 100, 150), 
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Text
        exp_text = self.font_small.render(
            f"XP: {exp_system.current_exp}/{exp_system.exp_to_next_level}", 
            True, (255, 255, 255)
        )
        text_rect = exp_text.get_rect()
        text_rect.center = (bar_x + bar_width // 2, bar_y + bar_height // 2)
        surface.blit(exp_text, text_rect)
    
    def draw_health_bar(self, surface, player):
        """Draw the player health bar at top center."""
        bar_width = 300
        bar_height = 30
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = 20
        
        # Background
        pygame.draw.rect(surface, (60, 0, 0), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Health fill
        health_ratio = player.health / player.max_health
        fill_width = int(bar_width * health_ratio)
        
        # Color based on health
        if health_ratio > 0.6:
            color = (0, 255, 0)
        elif health_ratio > 0.3:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        
        pygame.draw.rect(surface, color, 
                        (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, (150, 150, 150), 
                        (bar_x, bar_y, bar_width, bar_height), 3)
        
        # Text
        health_text = self.font_medium.render(
            f"HP: {int(player.health)}/{int(player.max_health)}", 
            True, (255, 255, 255)
        )
        text_rect = health_text.get_rect()
        text_rect.center = (bar_x + bar_width // 2, bar_y + bar_height // 2)
        surface.blit(health_text, text_rect)
    
    def draw_fps(self, surface, fps):
        """Draw FPS counter (for debugging)."""
        fps_text = self.font_small.render(f"FPS: {int(fps)}", True, (150, 150, 150))
        surface.blit(fps_text, (self.screen_width - 100, self.screen_height - 30))