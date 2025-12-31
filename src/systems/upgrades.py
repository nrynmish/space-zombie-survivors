"""
Upgrade definitions - all available upgrades in the game
"""


def get_all_upgrades():
    """Return list of all possible upgrades."""
    return [
        # Weapon Upgrades
        {
            'type': 'weapon_upgrade',
            'weapon': 'AutoGun',
            'name': 'Gun Upgrade',
            'icon': '🔫',
            'description': 'Upgrade your Auto Gun. Increases fire rate or adds more bullets!'
        },
        {
            'type': 'weapon_upgrade',
            'weapon': 'OrbitingDisc',
            'name': 'Disc Upgrade',
            'icon': '⚔️',
            'description': 'Upgrade your Orbiting Disc. Adds more discs or increases damage!'
        },
        
        # Stat Boosts
        {
            'type': 'stat_boost',
            'stat': 'max_health',
            'value': 20,
            'name': 'Max Health +20',
            'icon': '❤️',
            'description': 'Increase maximum health by 20. Also fully heals you!'
        },
        {
            'type': 'stat_boost',
            'stat': 'max_health',
            'value': 50,
            'name': 'Max Health +50',
            'icon': '💚',
            'description': 'Massive health boost! Gain 50 max HP and full heal!'
        },
        {
            'type': 'stat_boost',
            'stat': 'speed',
            'value': 50,
            'name': 'Movement Speed',
            'icon': '⚡',
            'description': 'Move 50 units faster. Dodge zombies more easily!'
        },
        {
            'type': 'stat_boost',
            'stat': 'speed',
            'value': 100,
            'name': 'Super Speed',
            'icon': '💨',
            'description': 'Major speed boost! Move 100 units faster!'
        },
        {
            'type': 'stat_boost',
            'stat': 'pickup_radius',
            'value': 40,
            'name': 'Magnet',
            'icon': '🧲',
            'description': 'Collect XP from further away. Increases pickup radius by 40!'
        },
        {
            'type': 'stat_boost',
            'stat': 'pickup_radius',
            'value': 80,
            'name': 'Super Magnet',
            'icon': '🌟',
            'description': 'Massive pickup range! Pull XP from across the screen!'
        },
        
        # Healing
        {
            'type': 'stat_boost',
            'stat': 'heal',
            'value': 50,
            'name': 'Health Potion',
            'icon': '🍷',
            'description': 'Restore 50 HP immediately. Great for emergencies!'
        },
        {
            'type': 'stat_boost',
            'stat': 'heal',
            'value': 100,
            'name': 'Full Heal',
            'icon': '✨',
            'description': 'Restore all health to maximum! Complete recovery!'
        },
    ]


def get_available_upgrades(player, weapons):
    """Filter upgrades based on current game state."""
    all_upgrades = get_all_upgrades()
    available = []
    
    for upgrade in all_upgrades:
        # Always allow weapon upgrades if weapon exists
        if upgrade['type'] == 'weapon_upgrade':
            weapon_name = upgrade['weapon']
            has_weapon = any(w.__class__.__name__ == weapon_name for w in weapons)
            if has_weapon:
                available.append(upgrade)
        
        # Allow stat boosts
        elif upgrade['type'] == 'stat_boost':
            # Don't offer full heal if already at max health
            if upgrade['stat'] == 'heal':
                if player.health < player.max_health:
                    available.append(upgrade)
            else:
                available.append(upgrade)
    
    return available