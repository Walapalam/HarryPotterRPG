"""
Spell system for the Harry Potter RPG game.
Contains the base Spell class and implementations of specific spells.
"""
from typing import Optional


class Spell:
    """Base class for all spells in the game."""
    
    def __init__(self, name: str, mana_cost: int, description: str, damage: int = 0, effect: Optional[str] = None):
        """
        Initialize a new spell.
        
        Args:
            name: Name of the spell
            mana_cost: Mana points required to cast the spell
            description: Description of what the spell does
            damage: Amount of damage the spell deals (if any)
            effect: Special effect the spell has (if any)
        """
        self.name = name
        self.mana_cost = mana_cost
        self.description = description
        self.damage = damage
        self.effect = effect
    
    def __str__(self) -> str:
        """Return a string representation of the spell."""
        return f"{self.name} (Mana: {self.mana_cost}) - {self.description}"
    
    def cast(self, caster: 'Character', target: Optional['Character'] = None) -> tuple[int, Optional[str]]:
        """
        Cast the spell, returning the damage dealt and any effects.
        
        Args:
            caster: The character casting the spell
            target: The target of the spell (if any)
            
        Returns:
            Tuple of (damage_dealt, effect_applied)
        """
        if caster.mana < self.mana_cost:
            return 0, "Not enough mana!"
        
        caster.mana -= self.mana_cost
        return self.damage, self.effect


# Pre-defined spells
LUMOS = Spell(
    name="Lumos",
    mana_cost=5,
    description="Creates a bright light from your wand",
    effect="illumination"
)

EXPELLIARMUS = Spell(
    name="Expelliarmus",
    mana_cost=20,
    description="Disarms your opponent",
    damage=15,
    effect="disarm"
)

STUPEFY = Spell(
    name="Stupefy",
    mana_cost=25,
    description="Stuns your opponent",
    damage=20,
    effect="stun"
)

PROTEGO = Spell(
    name="Protego",
    mana_cost=15,
    description="Creates a magical shield to protect yourself",
    effect="shield"
)

FLIPENDO = Spell(
    name="Flipendo",
    mana_cost=18,
    description="Knocks back your opponent",
    damage=12,
    effect="knockback"
)

EPISKEY = Spell(
    name="Episkey",
    mana_cost=30,
    description="Heals minor to moderate injuries",
    effect="heal"
)

# Dictionary of all available spells
ALL_SPELLS = {
    spell.name.lower(): spell
    for spell in [LUMOS, EXPELLIARMUS, STUPEFY, PROTEGO, FLIPENDO, EPISKEY]
}