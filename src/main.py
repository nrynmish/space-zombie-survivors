import pygame
import sys
import random

# Import configuration
from config import *

# Import entities
from entities.player import Player
from entities.zombie import Zombie
from entities.exp_gem import ExpGem
from entities.bullet import Bullet
from entities.boss_zombie import BossZombie

# Import systems
from systems.spawner import ZombieSpawner
from systems.experience import ExperienceSystem
from systems.particles import VoidParticle, create_death_particles, create_void_particles

# Import UI
from ui.hud import HUD
from ui.upgrade_menu import UpgradeMenu
from ui.main_menu import MainMenu

#Import weapons
from weapons.auto_gun import AutoGun
from weapons.orbiting_disc import OrbitingDisc

#Import upgrades
from systems.upgrades import get_available_upgrades


class Game:
    """Main game class that manages the game loop."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Zombie Survivors")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.paused = False
        self.game_over = False
        
        # Initialize systems
        self.player = Player((WIDTH // 2, HEIGHT // 2))
        self.spawner = ZombieSpawner(WIDTH, HEIGHT)
        self.exp_system = ExperienceSystem()
        self.hud = HUD(WIDTH, HEIGHT)
        self.upgrade_menu = UpgradeMenu(WIDTH, HEIGHT)
        self.main_menu = MainMenu(WIDTH, HEIGHT)    
        
        # Entity lists
        self.zombies = []
        self.bullets = []
        self.exp_gems = []
        self.particles = []
        
        #Boss 
        self.boss = None
        self.boss_spawned = False
        self.boss_spawn_time = 150  # Spawn boss after 150 seconds
        
        # Game stats
        self.game_time = 0
        self.kills = 0

        #Screen Shake
        self.screen_shake = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        
        # Weapon system (basic auto-gun for now)
        self.weapons = [
            AutoGun(self.player),
            OrbitingDisc(self.player)
        ] 
        
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.running = False
                    else:
                        self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.restart()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle main menu clicks
                if self.main_menu.active:
                    self.main_menu.handle_click(event.pos)
                # Handle upgrade menu clicks
                elif self.upgrade_menu.active:
                    self.upgrade_menu.handle_click(event.pos)
    
    def restart(self):
        """Restart the game."""
        self.__init__()
    
    def update(self, dt):
        """Update all game entities and systems."""
        if self.paused or self.game_over or self.upgrade_menu.active or self.main_menu.active:
            return
        
        # Update game time
        self.game_time += dt
        
        # Update player
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, dt)
        self.player.clamp(WIDTH, HEIGHT)
        self.player.update(dt)

         # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= dt * 10
            self.shake_offset_x = random.randint(-int(self.screen_shake), int(self.screen_shake))
            self.shake_offset_y = random.randint(-int(self.screen_shake), int(self.screen_shake))
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0
        
        # New Weapons update
        for weapon in self.weapons:
            new_bullets = weapon.update(dt, self.zombies)
            self.bullets.extend(new_bullets)
        
        # Spawn void particles around player
        if random.random() < 0.3:
            self.particles.extend(create_void_particles(
                self.player.rect.centerx, 
                self.player.rect.centery, 
                1
            ))
        
        # Spawn zombies
        if self.spawner.should_spawn(dt):
            self.zombies.append(self.spawner.spawn_zombie())

        # Spawn boss at specific time
        if not self.boss_spawned and self.game_time >= self.boss_spawn_time:
            self.spawn_boss()
        
        # Update zombies
        for zombie in self.zombies[:]:
            zombie.update(dt, self.player.rect.center)
            
            # Check collision with player
            if zombie.alive and self.player.rect.colliderect(zombie.rect):
                if self.player.take_damage(zombie.damage):
                    self.game_over = True
                else:
                    self.screen_shake = 10  # Trigger screen shake
        
        # Update boss
        if self.boss and self.boss.alive:
            self.boss.update(dt, self.player.rect.center)
            
            # Boss collision with player
            if self.boss.rect.colliderect(self.player.rect):
                if self.player.take_damage(self.boss.damage):
                    self.game_over = True
                else:
                    self.screen_shake = 15  # Bigger shake for boss!
            
            # Boss spawns minions
            if self.boss.should_spawn_minion():
                # Spawn 3 zombies around boss
                for i in range(5):
                    offset_x = random.randint(-100, 100)
                    offset_y = random.randint(-100, 100)
                    minion = Zombie(
                        self.boss.rect.centerx + offset_x,
                        self.boss.rect.centery + offset_y,
                        "fast"
                    )
                    self.zombies.append(minion)

        # Update bullets
        for bullet in self.bullets[:]:
            if not bullet.update(dt, WIDTH, HEIGHT):
                self.bullets.remove(bullet)
                continue
            
            # Check bullet-zombie collisions
            for zombie in self.zombies:
                if bullet.check_collision(zombie):
                    if not zombie.alive:
                        # Zombie died
                        self.kills += 1
                        # Drop exp gem
                        self.exp_gems.append(ExpGem(
                            zombie.rect.centerx,
                            zombie.rect.centery,
                            zombie.exp_value
                        ))
                        # Create death particles
                        self.particles.extend(create_death_particles(
                            zombie.rect.centerx,
                            zombie.rect.centery,
                            zombie.color,
                            count = 25
                        ))
                        self.zombies.remove(zombie)
                    break
                    
            # Check bullet-boss collision
            if self.boss and self.boss.alive and bullet.alive:
                if bullet.check_collision(self.boss):
                    if not self.boss.alive:
                        # BOSS DEFEATED!
                        self.kills += 1
                        # Huge XP drop
                        self.exp_gems.append(ExpGem(
                            self.boss.rect.centerx,
                            self.boss.rect.centery,
                            self.boss.exp_value
                        ))
                        # Massive particle explosion!
                        self.particles.extend(create_death_particles(
                            self.boss.rect.centerx,
                            self.boss.rect.centery,
                            self.boss.color,
                            count=50  # HUGE explosion!
                        ))
                        self.screen_shake = 30  # BIG shake!
                        self.boss = None

        # Update exp gems
        for gem in self.exp_gems[:]:
            if gem.update(dt, self.player.rect.center, self.player.pickup_radius):
                # Player collected the gem
                self.exp_gems.remove(gem)
                if self.exp_system.add_exp(gem.value):
                    # Level up!
                    self.on_level_up()
        
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
    

    def on_level_up(self):
        """Handle level up event."""
        # TODO: Show upgrade menu
        # For now, just give a stat boost
        available = get_available_upgrades(self.player, self.weapons)
        self.upgrade_menu.show(self.player, self.weapons, available)
        print(f"Level up! Now level {self.exp_system.level}")
    
    def spawn_boss(self):
        """Spawn the boss zombie!"""
        self.boss_spawned = True
        
        # Spawn boss at top center of screen
        boss_x = WIDTH // 2
        boss_y = -100
        
        self.boss = BossZombie(boss_x, boss_y)
        
        # Show warning message
        print("⚠️  BOSS INCOMING! ⚠️")

    def draw(self):
        """Draw all game entities."""
        # Clear screen with void color
        self.screen.fill(COLOR_BG)
        
        # If main menu is active, only draw menu
        if self.main_menu.active:
            self.main_menu.draw(self.screen)
            pygame.display.flip()
            return
        
        # Create a temporary surface for screen shake
        temp_surface = pygame.Surface((WIDTH, HEIGHT))
        temp_surface.fill(COLOR_BG)
        
        # Draw particles (behind everything)
        for particle in self.particles:
            particle.draw(temp_surface)
        
        # Draw exp gems
        for gem in self.exp_gems:
            gem.draw(temp_surface)
        
        # Draw zombies
        for zombie in self.zombies:
            zombie.draw(temp_surface)

        # Draw boss
        if self.boss and self.boss.alive:
            self.boss.draw(temp_surface)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(temp_surface)
        
        # Draw player
        self.player.draw(temp_surface)
        
        # Draw weapons (like orbiting disc)
        for weapon in self.weapons:
            weapon.draw(temp_surface)
        
        # Draw HUD (no shake on UI)
        self.hud.draw(temp_surface, self.player, self.exp_system, 
                     self.game_time, self.kills)
        self.hud.draw_fps(temp_surface, self.clock.get_fps())
        
        # Apply screen shake
        self.screen.blit(temp_surface, (self.shake_offset_x, self.shake_offset_y))
        
        # Draw pause overlay (no shake)
        if self.paused:
            self.draw_pause_screen()
        
        # Draw game over screen (no shake)
        if self.game_over:
            self.draw_game_over_screen()
        
        # Draw upgrade menu (on top of everything, no shake)
        self.upgrade_menu.draw(self.screen)
        
        pygame.display.flip()
    
    def draw_pause_screen(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont(None, 72)
        text = font.render("PAUSED", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, rect)
        
        font_small = pygame.font.SysFont(None, 36)
        text2 = font_small.render("Press ESC to resume", True, (200, 200, 200))
        rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        self.screen.blit(text2, rect2)
    
    def draw_game_over_screen(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((20, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont(None, 96)
        text = font.render("GAME OVER", True, (255, 50, 50))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        self.screen.blit(text, rect)
        
        font_medium = pygame.font.SysFont(None, 48)
        stats = [
            f"Survived: {int(self.game_time // 60)}:{int(self.game_time % 60):02d}",
            f"Level: {self.exp_system.level}",
            f"Kills: {self.kills}",
        ]
        
        y_offset = HEIGHT // 2
        for stat in stats:
            text = font_medium.render(stat, True, (255, 255, 255))
            rect = text.get_rect(center=(WIDTH // 2, y_offset))
            self.screen.blit(text, rect)
            y_offset += 50
        
        font_small = pygame.font.SysFont(None, 36)
        text2 = font_small.render("Press R to restart or ESC to quit", True, (200, 200, 200))
        rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.screen.blit(text2, rect2)
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()