"""
NPC system for the Harry Potter RPG game.
Contains the base NPC class and specific NPC implementations.
"""
import random
from typing import List, Optional
from spell import Spell, ALL_SPELLS


class Character:
    """Base class for all characters (players and NPCs)."""
    
    def __init__(self, name: str, max_health: int = 100, max_mana: int = 100):
        self.name = name
        self.max_health = max_health
        self.max_mana = max_mana
        self.health = max_health
        self.mana = max_mana
        self.known_spells: List[Spell] = []
    
    def is_alive(self) -> bool:
        """Check if the character is still alive."""
        return self.health > 0
    
    def take_damage(self, amount: int) -> None:
        """Take damage, ensuring health doesn't go below 0."""
        self.health = max(0, self.health - amount)
    
    def heal(self, amount: int) -> None:
        """Heal the character, not exceeding max health."""
        self.health = min(self.max_health, self.health + amount)
    
    def restore_mana(self, amount: int) -> None:
        """Restore mana, not exceeding max mana."""
        self.mana = min(self.max_mana, self.mana + amount)


class NPC(Character):
    """Class representing non-player characters that can be dueled."""
    
    def __init__(self, name: str, difficulty: str = "normal"):
        """
        Initialize an NPC with given difficulty level.
        
        Args:
            name: Name of the NPC
            difficulty: "easy", "normal", or "hard"
        """
        # Adjust stats based on difficulty
        health_map = {"easy": 80, "normal": 100, "hard": 120}
        mana_map = {"easy": 80, "normal": 100, "hard": 120}
        
        super().__init__(
            name=name,
            max_health=health_map.get(difficulty, 100),
            max_mana=mana_map.get(difficulty, 100)
        )
        
        # Give the NPC some spells based on difficulty
        spell_count = {"easy": 2, "normal": 3, "hard": 4}
        self.known_spells = random.sample(list(ALL_SPELLS.values()), spell_count.get(difficulty, 3))
    
    def choose_spell(self) -> Optional[Spell]:
        """Choose a random spell that the NPC can cast."""
        castable_spells = [spell for spell in self.known_spells if spell.mana_cost <= self.mana]
        return random.choice(castable_spells) if castable_spells else None


# Pre-defined NPCs for dueling
TRAINING_DUMMY = NPC("Training Dummy", "easy")
STUDENT_DUELIST = NPC("Student Duelist", "normal")
DARK_WIZARD = NPC("Dark Wizard", "hard")