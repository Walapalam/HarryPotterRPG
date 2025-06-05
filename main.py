"""
Main entry point for the Harry Potter RPG game.
Contains the game loop and main menu system.
"""
import random
import json
import os
from typing import Optional

from player import Player
from spell import ALL_SPELLS, Spell
from npcs import TRAINING_DUMMY, STUDENT_DUELIST, DARK_WIZARD, NPC
from utils import clear_screen, get_valid_input, sorting_hat_quiz, generate_random_event

SAVE_FILE = "savegame.json"


class HogwartsRPG:
    """Main game class that handles the game loop and state."""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.running = True
        
    def save_game(self) -> None:
        """Save the current game state to a file."""
        if not self.player:
            print("No game in progress to save!")
            return
            
        save_data = self.player.to_dict()
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(save_data, f)
            print("Game saved successfully!")
        except Exception as e:
            print(f"Error saving game: {e}")
            
    def load_game(self) -> bool:
        """Load a saved game from file."""
        if not os.path.exists(SAVE_FILE):
            print("No saved game found!")
            return False
            
        try:
            with open(SAVE_FILE, 'r') as f:
                save_data = json.load(f)
            self.player = Player.from_dict(save_data)
            print("Game loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def start_new_game(self) -> None:
        """Start a new game by creating a character."""
        clear_screen()
        print("Welcome to Hogwarts School of Witchcraft and Wizardry!")
        
        # Get player name
        name = input("Enter your character's name: ").strip()
        if not name:
            return
            
        print(f"\nWelcome, {name}!")
        print("\nNow, let the sorting begin!")
        house = sorting_hat_quiz()
        print(f"\nThe Sorting Hat has decided... {house}!")
        
        self.player = Player(name, house)
        # Give the player their first spell
        self.player.learn_spell(ALL_SPELLS["lumos"])
        
        # Show initial stats
        self.show_stats()
    
    def show_stats(self) -> None:
        """Display character stats."""
        if not self.player:
            return
        
        stats = self.player.get_stats()
        print("\n=== Character Stats ===")
        print(f"Name: {stats['Name']}")
        print(f"House: {stats['House']}")
        print(f"Health: {stats['Health']}")
        print(f"Mana: {stats['Mana']}")
        print(f"Knowledge: {stats['Knowledge']}")
        print(f"House Points: {stats['House Points']}")
        print("\nKnown Spells:")
        for spell in stats['Known Spells']:
            print(f"- {spell}")
    
    def attend_class(self) -> None:
        """Simulate attending a class to learn new spells."""
        if not self.player:
            return
        
        clear_screen()
        print("=== Attending Class ===")
        
        # Random chance to learn a new spell
        available_spells = [
            spell for spell in ALL_SPELLS.values()
            if spell not in self.player.known_spells
        ]
        
        if not available_spells:
            print("You already know all available spells!")
        else:
            spell = random.choice(available_spells)
            if self.player.learn_spell(spell):
                print(f"You learned the spell: {spell.name}!")
                self.player.gain_knowledge(10)
                self.player.award_house_points(5)
                self.show_stats()
    
    def cast_spell(self) -> None:
        """Cast a spell outside of combat."""
        if not self.player:
            return
        
        clear_screen()
        print("=== Cast a Spell ===")
        
        if not self.player.known_spells:
            print("You don't know any spells yet!")
            return
        
        # Show available spells
        print("\nAvailable spells:")
        for i, spell in enumerate(self.player.known_spells, 1):
            print(f"{i}. {spell.name}")
        
        choice = get_valid_input("\nChoose a spell (number): ", [str(i) for i in range(1, len(self.player.known_spells) + 1)])
        spell = list(self.player.known_spells)[int(choice) - 1]
        
        damage, effect = spell.cast(self.player)
        print(f"\nYou cast {spell.name}!")
        if effect:
            print(f"Effect: {effect}")
        self.show_stats()
    
    def explore(self) -> None:
        """Explore Hogwarts for random events."""
        if not self.player:
            return
        
        clear_screen()
        print("=== Exploring Hogwarts ===")
        
        event, points = generate_random_event()
        print(event)
        self.player.award_house_points(points)
        
        # Random mana restoration
        mana_restored = random.randint(5, 15)
        self.player.restore_mana(mana_restored)
        print(f"You feel refreshed! (+{mana_restored} mana)")
        
        self.show_stats()
    
    def duel(self) -> None:
        """Start a duel with an NPC."""
        if not self.player:
            return
        
        clear_screen()
        print("=== Wizard's Duel ===")
        
        # Choose opponent
        opponents = {
            "1": TRAINING_DUMMY,
            "2": STUDENT_DUELIST,
            "3": DARK_WIZARD
        }
        
        print("Choose your opponent:")
        for num, npc in opponents.items():
            print(f"{num}. {npc.name}")
        
        choice = get_valid_input("Your choice (1-3): ", list(opponents.keys()))
        opponent = opponents[choice]
        self._run_duel(opponent)
    
    def _run_duel(self, opponent: NPC) -> None:
        """Run the actual duel mechanics."""
        print(f"\nDuel start! {self.player.name} vs {opponent.name}")
        
        while self.player.is_alive() and opponent.is_alive():
            # Player's turn
            print(f"\nYour HP: {self.player.health}/{self.player.max_health}")
            print(f"Opponent HP: {opponent.health}/{opponent.max_health}")
            print("\nYour turn! Choose a spell:")
            
            # Show available spells
            for i, spell in enumerate(self.player.known_spells, 1):
                print(f"{i}. {spell.name}")
            
            choice = get_valid_input("Choose a spell (number): ", [str(i) for i in range(1, len(self.player.known_spells) + 1)])
            spell = list(self.player.known_spells)[int(choice) - 1]
            
            damage, effect = spell.cast(self.player, opponent)
            
            print(f"\nYou cast {spell.name}!")
            if damage:
                opponent.take_damage(damage)
                print(f"Dealt {damage} damage!")
            if effect:
                print(f"Applied effect: {effect}")
            
            if not opponent.is_alive():
                print(f"\nVictory! You defeated {opponent.name}!")
                self.player.award_house_points(20)
                break
            
            # Opponent's turn
            print(f"\n{opponent.name}'s turn!")
            spell = opponent.choose_spell()
            
            if spell:
                damage, effect = spell.cast(opponent, self.player)
                print(f"{opponent.name} casts {spell.name}!")
                if damage:
                    self.player.take_damage(damage)
                    print(f"You take {damage} damage!")
                if effect:
                    print(f"Effect applied: {effect}")
            else:
                print(f"{opponent.name} is too exhausted to cast a spell!")
            
            if not self.player.is_alive():
                print("\nDefeat! You lost the duel!")
                self.player.award_house_points(-10)
                break
            
            input("\nPress Enter to continue...")
            clear_screen()
        
        # Restore some health and mana after the duel
        self.player.heal(30)
        self.player.restore_mana(30)
        self.show_stats()
    
    def main_menu(self) -> None:
        """Display and handle the main menu."""
        while self.running:
            clear_screen()
            print("=== Hogwarts RPG ===")
            
            if not self.player:
                print("\n1. Start New Game")
                print("2. Load Game")
                print("3. Quit")
                
                choice = get_valid_input("\nChoose an option (1-3): ", ["1", "2", "3"])
                
                if choice == "1":
                    self.start_new_game()
                elif choice == "2":
                    self.load_game()
                elif choice == "3":
                    self.running = False
            else:
                print("\n1. Explore Hogwarts")
                print("2. Attend Class")
                print("3. Cast Spell")
                print("4. Duel")
                print("5. View Stats")
                print("6. Save Game")
                print("7. Quit")
                
                choice = get_valid_input("\nChoose an option (1-7): ", [str(i) for i in range(1, 8)])
                
                if choice == "1":
                    self.explore()
                elif choice == "2":
                    self.attend_class()
                elif choice == "3":
                    self.cast_spell()
                elif choice == "4":
                    self.duel()
                elif choice == "5":
                    self.show_stats()
                elif choice == "6":
                    self.save_game()
                elif choice == "7":
                    self.running = False
                
                if choice != "7":
                    input("\nPress Enter to continue...")


if __name__ == "__main__":
    game = HogwartsRPG()
    game.main_menu()