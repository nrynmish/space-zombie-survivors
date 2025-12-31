"""
Upgrade Menu - Shows upgrade choices when player levels up
"""
import pygame
import random
from config import *


class UpgradeMenu:
    """Displays upgrade choices when player levels up."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 32)
        self.font_small = pygame.font.SysFont(None, 24)
        
        self.active = False
        self.upgrade_options = []
        self.selected_upgrade = None
        
        # Card dimensions
        self.card_width = 280
        self.card_height = 400
        self.card_spacing = 40
        
    def show(self, player, weapons, available_upgrades):
        """Show the upgrade menu with 3 random options."""
        self.active = True
        self.selected_upgrade = None
        
        # Pick 3 random upgrades
        if len(available_upgrades) <= 3:
            self.upgrade_options = available_upgrades[:]
        else:
            self.upgrade_options = random.sample(available_upgrades, 3)
        
        # Store references for applying upgrades
        self.player = player
        self.weapons = weapons
    
    def handle_click(self, mouse_pos):
        """Check if player clicked on an upgrade card."""
        if not self.active:
            return None
        
        # Calculate card positions
        total_width = (self.card_width * 3) + (self.card_spacing * 2)
        start_x = (self.screen_width - total_width) // 2
        card_y = (self.screen_height - self.card_height) // 2
        
        for i, upgrade in enumerate(self.upgrade_options):
            card_x = start_x + (i * (self.card_width + self.card_spacing))
            card_rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)
            
            if card_rect.collidepoint(mouse_pos):
                self.selected_upgrade = upgrade
                self.apply_upgrade(upgrade)
                self.active = False
                return upgrade
        
        return None
    
    def apply_upgrade(self, upgrade):
        """Apply the selected upgrade."""
        upgrade_type = upgrade['type']
        
        if upgrade_type == 'weapon_upgrade':
            # Upgrade existing weapon
            weapon_name = upgrade['weapon']
            for weapon in self.weapons:
                if weapon.__class__.__name__ == weapon_name:
                    weapon.upgrade()
                    break
        
        elif upgrade_type == 'new_weapon':
            # Add new weapon (we'll implement this next)
            pass
        
        elif upgrade_type == 'stat_boost':
            # Boost player stats
            stat = upgrade['stat']
            value = upgrade['value']
            
            if stat == 'max_health':
                self.player.max_health += value
                self.player.health = self.player.max_health
            elif stat == 'speed':
                self.player.speed += value
            elif stat == 'pickup_radius':
                self.player.pickup_radius += value
            elif stat == 'heal':
                self.player.health = min(self.player.health + value, self.player.max_health)
    
    def draw(self, surface):
        """Draw the upgrade menu."""
        if not self.active:
            return
        
        # Draw overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Draw title
        title = self.font_large.render("LEVEL UP!", True, (255, 255, 100))
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        surface.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Choose an upgrade:", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 160))
        surface.blit(subtitle, subtitle_rect)
        
        # Draw upgrade cards
        total_width = (self.card_width * 3) + (self.card_spacing * 2)
        start_x = (self.screen_width - total_width) // 2
        card_y = (self.screen_height - self.card_height) // 2
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, upgrade in enumerate(self.upgrade_options):
            card_x = start_x + (i * (self.card_width + self.card_spacing))
            self.draw_card(surface, upgrade, card_x, card_y, mouse_pos)
    
    def draw_card(self, surface, upgrade, x, y, mouse_pos):
        """Draw a single upgrade card."""
        card_rect = pygame.Rect(x, y, self.card_width, self.card_height)
        
        # Check if mouse is hovering
        is_hover = card_rect.collidepoint(mouse_pos)
        
        # Card background
        if is_hover:
            bg_color = (60, 60, 80)
            border_color = (150, 200, 255)
            border_width = 4
        else:
            bg_color = (40, 40, 60)
            border_color = (100, 100, 150)
            border_width = 2
        
        pygame.draw.rect(surface, bg_color, card_rect)
        pygame.draw.rect(surface, border_color, card_rect, border_width)
        
        # Icon/emoji area
        icon_y = y + 30
        icon_text = self.font_large.render(upgrade.get('icon', '⚔'), True, (255, 255, 255))
        icon_rect = icon_text.get_rect(center=(x + self.card_width // 2, icon_y))
        surface.blit(icon_text, icon_rect)
        
        # Title
        title_y = icon_y + 60
        title_text = self.font_medium.render(upgrade['name'], True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(x + self.card_width // 2, title_y))
        surface.blit(title_text, title_rect)
        
        # Description (word wrap)
        desc_y = title_y + 50
        self.draw_wrapped_text(surface, upgrade['description'], 
                              x + 20, desc_y, self.card_width - 40, 
                              (200, 200, 200))
        
        # Hover hint
        if is_hover:
            hint = self.font_small.render("Click to select", True, (150, 200, 255))
            hint_rect = hint.get_rect(center=(x + self.card_width // 2, y + self.card_height - 30))
            surface.blit(hint, hint_rect)
    
    def draw_wrapped_text(self, surface, text, x, y, max_width, color):
        """Draw text with word wrapping."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.font_small.render(test_line, True, color)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        for i, line in enumerate(lines):
            line_surface = self.font_small.render(line, True, color)
            surface.blit(line_surface, (x, y + i * 30))