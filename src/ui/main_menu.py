"""
Main Menu - Title screen with start button
"""
import pygame
from config import *


class MainMenu:
    """Main menu / title screen."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_title = pygame.font.SysFont(None, 96)
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)
        
        self.active = True
        
        # Button
        self.button_width = 300
        self.button_height = 80
        self.button_x = (screen_width - self.button_width) // 2
        self.button_y = screen_height // 2 + 50
        self.button_rect = pygame.Rect(self.button_x, self.button_y, 
                                       self.button_width, self.button_height)
    
    def handle_click(self, mouse_pos):
        """Check if start button was clicked."""
        if self.button_rect.collidepoint(mouse_pos):
            self.active = False
            return True  # Start game
        return False
    
    def draw(self, surface):
        """Draw the main menu."""
        if not self.active:
            return
        
        # Background
        surface.fill(COLOR_BG)
        
        # Draw some decorative particles/stars
        for i in range(50):
            x = (i * 137) % self.screen_width
            y = (i * 193) % self.screen_height
            size = (i % 3) + 1
            pygame.draw.circle(surface, (100, 100, 150), (x, y), size)
        
        # Title
        title = self.font_title.render("SPACE ZOMBIE", True, (255, 100, 100))
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        surface.blit(title, title_rect)
        
        title2 = self.font_title.render("SURVIVORS", True, (100, 200, 255))
        title2_rect = title2.get_rect(center=(self.screen_width // 2, 240))
        surface.blit(title2, title2_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("Fight endless hordes in the void!", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 320))
        surface.blit(subtitle, subtitle_rect)
        
        # Start button
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.button_rect.collidepoint(mouse_pos)
        
        if is_hover:
            button_color = (80, 80, 120)
            border_color = (150, 200, 255)
            text_color = (255, 255, 255)
        else:
            button_color = (60, 60, 90)
            border_color = (100, 150, 200)
            text_color = (200, 200, 200)
        
        pygame.draw.rect(surface, button_color, self.button_rect)
        pygame.draw.rect(surface, border_color, self.button_rect, 4)
        
        button_text = self.font_large.render("START GAME", True, text_color)
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        surface.blit(button_text, button_text_rect)
        
        # Controls info
        controls_y = self.screen_height - 180
        controls = [
            "Controls:",
            "WASD / Arrow Keys - Move",
            "Mouse - Auto-aim (weapons fire automatically)",
            "ESC - Pause"
        ]
        
        for i, text in enumerate(controls):
            color = (150, 150, 150) if i == 0 else (120, 120, 120)
            font = self.font_small if i > 0 else self.font_medium
            control_text = font.render(text, True, color)
            control_rect = control_text.get_rect(center=(self.screen_width // 2, controls_y + i * 30))
            surface.blit(control_text, control_rect)
        
        # Theme info
        theme_text = self.font_small.render("Game Jam Theme: Void, Yet Alive", True, (100, 100, 150))
        theme_rect = theme_text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
        surface.blit(theme_text, theme_rect)