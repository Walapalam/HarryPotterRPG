"""
Unit tests for the Hogwarts RPG game.
"""
import unittest
import os
import json
from player import Player
from spell import ALL_SPELLS, Spell
from npcs import TRAINING_DUMMY
from main import HogwartsRPG, SAVE_FILE

class TestHogwartsRPG(unittest.TestCase):
    def setUp(self):
        self.player = Player("Test Wizard", "Gryffindor")
    
    def test_player_creation(self):
        """Test that player is created with correct initial values."""
        self.assertEqual(self.player.name, "Test Wizard")
        self.assertEqual(self.player.house, "Gryffindor")
        self.assertEqual(self.player.health, self.player.max_health)
        self.assertEqual(self.player.mana, self.player.max_mana)
        self.assertEqual(len(self.player.known_spells), 0)
    
    def test_learning_spell(self):
        """Test that player can learn spells correctly."""
        spell = ALL_SPELLS["lumos"]
        self.player.learn_spell(spell)
        self.assertIn(spell, self.player.known_spells)
        
        # Test learning the same spell twice
        result = self.player.learn_spell(spell)
        self.assertFalse(result)  # Should return False when trying to learn known spell
    
    def test_combat_mechanics(self):
        """Test basic combat mechanics."""
        dummy = TRAINING_DUMMY
        spell = ALL_SPELLS["stupefy"]
        self.player.learn_spell(spell)
        
        initial_health = dummy.health
        damage, _ = spell.cast(self.player, dummy)
        dummy.take_damage(damage)
        
        self.assertLess(dummy.health, initial_health)

    def test_new_spells(self):
        """Test the functionality of the new spells."""
        dummy = TRAINING_DUMMY
        initial_health = dummy.health
        initial_mana = self.player.mana

        # Test Flipendo
        flipendo = ALL_SPELLS["flipendo"]
        self.player.learn_spell(flipendo)
        damage, effect = flipendo.cast(self.player, dummy)
        dummy.take_damage(damage)
        
        self.assertEqual(effect, "knockback")
        self.assertEqual(damage, 12)
        self.assertEqual(self.player.mana, initial_mana - flipendo.mana_cost)
        self.assertLess(dummy.health, initial_health)

        # Test Protego
        protego = ALL_SPELLS["protego"]
        self.player.learn_spell(protego)
        damage, effect = protego.cast(self.player)
        
        self.assertEqual(effect, "shield")
        self.assertEqual(damage, 0)

        # Test Episkey
        episkey = ALL_SPELLS["episkey"]
        self.player.learn_spell(episkey)
        damage, effect = episkey.cast(self.player)
        
        self.assertEqual(effect, "heal")
        self.assertEqual(damage, 0)

    def test_spell_mana_costs(self):
        """Test that spells require and consume the correct amount of mana."""
        # Set player's mana to a low value
        self.player.mana = 10
        
        # Try to cast Episkey (costs 30 mana)
        episkey = ALL_SPELLS["episkey"]
        self.player.learn_spell(episkey)
        damage, effect = episkey.cast(self.player)
        
        # Should fail due to insufficient mana
        self.assertEqual(effect, "Not enough mana!")
        self.assertEqual(damage, 0)
        self.assertEqual(self.player.mana, 10)  # Mana should not be deducted

    def test_save_load_game(self):
        """Test saving and loading game state."""
        # Create a game instance with some state
        game = HogwartsRPG()
        game.player = self.player
        game.player.learn_spell(ALL_SPELLS["lumos"])
        game.player.health = 50
        game.player.mana = 75
        game.player.knowledge = 100
        game.player.house_points = 50
        
        # Save the game
        game.save_game()
        self.assertTrue(os.path.exists(SAVE_FILE))
        
        # Create a new game instance and load the save
        new_game = HogwartsRPG()
        self.assertTrue(new_game.load_game())
        
        # Verify loaded state matches original
        self.assertEqual(new_game.player.name, self.player.name)
        self.assertEqual(new_game.player.house, self.player.house)
        self.assertEqual(new_game.player.health, 50)
        self.assertEqual(new_game.player.mana, 75)
        self.assertEqual(new_game.player.knowledge, 100)
        self.assertEqual(new_game.player.house_points, 50)
        self.assertEqual(len(new_game.player.known_spells), 1)
        self.assertEqual(new_game.player.known_spells[0].name, "Lumos")
        
        # Clean up
        os.remove(SAVE_FILE)
        
    def test_status_effects(self):
        """Test status effect application and clearing."""
        # Test shield effect
        protego = ALL_SPELLS["protego"]
        self.player.learn_spell(protego)
        _, effect = protego.cast(self.player, self.player)
        
        self.assertEqual(effect, "shield")
        self.assertTrue(self.player.shield_active)
        self.assertIn("Shield", self.player.get_status_effects())
        
        # Test that shield reduces damage
        initial_health = self.player.health
        dummy = TRAINING_DUMMY
        stupefy = ALL_SPELLS["stupefy"]
        damage = 20  # Stupefy's damage
        actual_damage = self.player.take_damage(damage)
        
        self.assertEqual(actual_damage, damage // 2)  # Shield should halve damage
        self.assertEqual(self.player.health, initial_health - (damage // 2))
        self.assertFalse(self.player.shield_active)  # Shield should break after use
        
        # Test stun effect
        self.player.learn_spell(stupefy)
        _, effect = stupefy.cast(self.player, dummy)
        
        self.assertEqual(effect, "stun")
        self.assertIn("Stunned", dummy.get_status_effects())
        
        # Test that stunned characters can't cast spells
        _, effect = stupefy.cast(dummy, self.player)
        self.assertEqual(effect, "Cannot cast while stunned!")
        
        # Test clearing effects
        dummy.clear_effects()
        self.assertEqual(len(dummy.get_status_effects()), 0)
        self.assertFalse(dummy.is_stunned)
    
    def test_mana_management(self):
        """Test mana consumption and replenishment."""
        initial_mana = self.player.mana
        
        # Test mana consumption
        stupefy = ALL_SPELLS["stupefy"]
        self.player.learn_spell(stupefy)
        stupefy.cast(self.player, TRAINING_DUMMY)
        
        self.assertEqual(self.player.mana, initial_mana - stupefy.mana_cost)
        
        # Test mana replenishment
        replenish_amount = 30
        self.player.restore_mana(replenish_amount)
        expected_mana = min(self.player.max_mana, initial_mana - stupefy.mana_cost + replenish_amount)
        
        self.assertEqual(self.player.mana, expected_mana)
        
        # Test mana cap at max_mana
        self.player.restore_mana(1000)
        self.assertEqual(self.player.mana, self.player.max_mana)
        
        # Test casting with insufficient mana
        self.player.mana = 5  # Set to very low value
        _, effect = stupefy.cast(self.player, TRAINING_DUMMY)
        self.assertEqual(effect, "Not enough mana!")
        self.assertEqual(self.player.mana, 5)  # Mana shouldn't be deducted on failed cast