"""
Main entry point for the Harry Potter RPG game.
Contains the game loop and main menu system.
"""
import random
from typing import Optional

from player import Player
from spell import ALL_SPELLS, Spell
from npcs import TRAINING_DUMMY, STUDENT_DUELIST, DARK_WIZARD, NPC
from utils import clear_screen, get_valid_input, sorting_hat_quiz, generate_random_event


class HogwartsRPG:
    """Main game class that handles the game loop and state."""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.running = True
    
    def start_new_game(self) -> None:
        """Start a new game by creating a character."""
        clear_screen()
        print("Welcome to Hogwarts School of Witchcraft and Wizardry!")
        name = input("Enter your character's name: ").strip()
        
        print("\nNow, let the sorting begin!")
        house = sorting_hat_quiz()
        print(f"\nThe Sorting Hat has decided... {house}!")
        
        self.player = Player(name, house)
        # Give the player their first spell
        self.player.learn_spell(ALL_SPELLS["lumos"])
    
    def show_stats(self) -> None:
        """Display character stats."""
        if not self.player:
            return
        
        clear_screen()
        print("=== Character Stats ===")
        for stat, value in self.player.get_stats().items():
            print(f"{stat}: {value}")
        input("\nPress Enter to continue...")
    
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
            
        input("\nPress Enter to continue...")
    
    def cast_spell(self) -> None:
        """Cast a spell outside of combat."""
        if not self.player:
            return
        
        clear_screen()
        print("=== Cast a Spell ===")
        
        if not self.player.known_spells:
            print("You don't know any spells yet!")
            input("\nPress Enter to continue...")
            return
        
        print("Known spells:")
        for i, spell in enumerate(self.player.known_spells, 1):
            print(f"{i}. {spell}")
        
        valid_inputs = [str(i) for i in range(1, len(self.player.known_spells) + 1)]
        choice = get_valid_input("Choose a spell to cast (or 'q' to cancel): ", valid_inputs + ['q'])
        
        if choice == 'q':
            return
            
        spell = self.player.known_spells[int(choice) - 1]
        damage, effect = spell.cast(self.player)
        
        print(f"\nYou cast {spell.name}!")
        if effect:
            print(f"Effect: {effect}")
        
        input("\nPress Enter to continue...")
    
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
        
        input("\nPress Enter to continue...")
    
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
        
        choice = get_valid_input("Select opponent (or 'q' to cancel): ", list(opponents.keys()) + ['q'])
        if choice == 'q':
            return
        
        opponent = opponents[choice]
        self._run_duel(opponent)
    
    def _run_duel(self, opponent: NPC) -> None:
        """Run the actual duel mechanics."""
        print(f"\nDuel start! {self.player.name} vs {opponent.name}")
        
        while self.player.is_alive() and opponent.is_alive():
            # Player's turn
            print(f"\nYour HP: {self.player.health}/{self.player.max_health}")
            print(f"Opponent HP: {opponent.health}/{opponent.max_health}")
            print("\nYour turn! Known spells:")
            
            for i, spell in enumerate(self.player.known_spells, 1):
                print(f"{i}. {spell}")
            
            valid_inputs = [str(i) for i in range(1, len(self.player.known_spells) + 1)]
            choice = get_valid_input("Choose your spell: ", valid_inputs)
            
            spell = self.player.known_spells[int(choice) - 1]
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
        
        # Restore some health and mana after the duel
        self.player.heal(30)
        self.player.restore_mana(30)
        input("\nPress Enter to continue...")
    
    def main_menu(self) -> None:
        """Display and handle the main menu."""
        while self.running:
            clear_screen()
            print("=== Hogwarts RPG ===")
            
            if not self.player:
                print("1. Start New Game")
                print("0. Quit")
                
                choice = get_valid_input("Choose an option: ", ['0', '1'])
                
                if choice == '0':
                    self.running = False
                elif choice == '1':
                    self.start_new_game()
            
            else:
                print(f"Playing as: {self.player.name} of {self.player.house}")
                print("\n1. View Character Stats")
                print("2. Attend Class")
                print("3. Cast a Spell")
                print("4. Explore Hogwarts")
                print("5. Wizard's Duel")
                print("0. Quit")
                
                choice = get_valid_input("Choose an option: ", ['0', '1', '2', '3', '4', '5'])
                
                if choice == '0':
                    self.running = False
                elif choice == '1':
                    self.show_stats()
                elif choice == '2':
                    self.attend_class()
                elif choice == '3':
                    self.cast_spell()
                elif choice == '4':
                    self.explore()
                elif choice == '5':
                    self.duel()


if __name__ == "__main__":
    game = HogwartsRPG()
    game.main_menu()