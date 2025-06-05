"""
Player system for the Harry Potter RPG game.
Contains the Player class which extends the base Character class.
"""
from typing import List, Dict, Any
from npcs import Character
from spell import Spell


class Player(Character):
    """Class representing the player character."""
    
    def __init__(self, name: str, house: str):
        """
        Initialize a new player.
        
        Args:
            name: Player's name
            house: Hogwarts house (Gryffindor, Slytherin, Hufflepuff, or Ravenclaw)
        """
        # Apply house-based stat bonuses
        house_bonuses = {
            "gryffindor": {"health": 120, "mana": 100},  # Brave - more health
            "slytherin": {"health": 100, "mana": 120},   # Cunning - more mana
            "hufflepuff": {"health": 110, "mana": 110},  # Balanced
            "ravenclaw": {"health": 90, "mana": 130},    # Wise - most mana
        }
        
        stats = house_bonuses.get(house.lower(), {"health": 100, "mana": 100})
        super().__init__(name=name, max_health=stats["health"], max_mana=stats["mana"])
        
        self.house = house
        self.knowledge = 0
        self.house_points = 0
        self.inventory: List[str] = ["Wand", "Textbooks"]
    
    def learn_spell(self, spell: Spell) -> bool:
        """
        Learn a new spell if not already known.
        
        Returns:
            bool: True if spell was learned, False if already known
        """
        if spell not in self.known_spells:
            self.known_spells.append(spell)
            return True
        return False
    
    def gain_knowledge(self, amount: int) -> None:
        """Gain knowledge points from attending classes."""
        self.knowledge += amount
    
    def award_house_points(self, points: int) -> None:
        """Award or deduct house points."""
        self.house_points += points
    
    def get_stats(self) -> Dict[str, Any]:
        """Get all player stats as a dictionary."""
        return {
            "Name": self.name,
            "House": self.house,
            "Health": f"{self.health}/{self.max_health}",
            "Mana": f"{self.mana}/{self.max_mana}",
            "Knowledge": self.knowledge,
            "House Points": self.house_points,
            "Known Spells": [spell.name for spell in self.known_spells],
            "Inventory": self.inventory
        }