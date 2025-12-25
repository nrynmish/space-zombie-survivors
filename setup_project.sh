#!/bin/bash

# Project setup script for Space Zombie Survivors

echo "🚀 Setting up Space Zombie Survivors project structure..."

# Create main directories
mkdir -p src/entities
mkdir -p src/weapons
mkdir -p src/systems
mkdir -p src/ui
mkdir -p assets/sprites
mkdir -p assets/effects
mkdir -p assets/ui
mkdir -p audio/effects
mkdir -p audio/music
mkdir -p docs

# Create Python files with basic structure
cat > src/config.py << 'PYEOF'
"""
Game configuration and constants
"""
# Window settings
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Player settings
PLAYER_SIZE = 32
PLAYER_SPEED = 300
PLAYER_MAX_HEALTH = 100
PLAYER_PICKUP_RADIUS = 80

# Zombie settings
ZOMBIE_SIZE = 28
ZOMBIE_SPEED = 80
ZOMBIE_SPAWN_RATE = 1.0  # seconds between spawns
ZOMBIE_BASE_HEALTH = 50

# Weapon settings
BULLET_SPEED = 500
BULLET_DAMAGE = 25
DISC_RADIUS = 100
DISC_ROTATION_SPEED = 180  # degrees per second
DISC_DAMAGE = 15

# Experience settings
EXP_BASE_VALUE = 10
EXP_TO_LEVEL = 100
EXP_LEVEL_MULTIPLIER = 1.2

# Colors
COLOR_BG = (20, 0, 40)
COLOR_PLAYER = (240, 240, 240)
COLOR_ZOMBIE = (50, 150, 50)
COLOR_BULLET = (255, 200, 100)
COLOR_EXP = (100, 255, 255)
COLOR_VOID = (80, 20, 120)
PYEOF

cat > src/entities/__init__.py << 'PYEOF'
"""Entity classes"""
from .player import Player
from .zombie import Zombie
from .exp_gem import ExpGem
from .bullet import Bullet
PYEOF

cat > src/weapons/__init__.py << 'PYEOF'
"""Weapon classes"""
from .weapon_base import Weapon
from .auto_gun import AutoGun
from .orbiting_disc import OrbitingDisc
PYEOF

cat > src/systems/__init__.py << 'PYEOF'
"""Game systems"""
from .experience import ExperienceSystem
from .spawner import ZombieSpawner
from .particles import VoidParticle
PYEOF

cat > src/ui/__init__.py << 'PYEOF'
"""UI classes"""
from .hud import HUD
from .upgrade_menu import UpgradeMenu
PYEOF

# Create empty __init__.py files
touch src/__init__.py

# Create requirements.txt
cat > requirements.txt << 'REQEOF'
pygame>=2.5.0
REQEOF

# Create README
cat > README.md << 'READEOF'
# Space Zombie Survivors 🧟‍♂️🚀

A space-themed survivor-like game created for the game jam (Dec 25-31, 2024).

## Theme Implementation
- **Void, Yet Alive**: Zombies floating in the void of space
- **Singularity**: Boss fights as singularity events
- **Rules are meant to be broken**: Overpowered upgrade combinations

## Gameplay
Survive endless waves of space zombies! Collect experience to level up and choose powerful upgrades. Build your ultimate weapon combination!

### Controls
- **WASD / Arrow Keys**: Move
- **Mouse**: Aim (weapons auto-fire)
- **ESC**: Pause

## Development
Built with Python and Pygame.

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Credits
- Game Development: [Your Name]
- Framework: Pygame
- Created for: [Jam Name] Game Jam
READEOF

# Create .gitignore
cat > .gitignore << 'GITEOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Game specific
*.log
saves/
GITEOF

echo "✅ Project structure created!"
echo ""
echo "📁 Directory tree:"
tree -L 3 -I 'venv|__pycache__' 2>/dev/null || find . -type d -not -path '*/venv/*' -not -path '*/__pycache__/*' | head -20

