"""
Unit tests for the Hogwarts RPG game.
"""
import unittest
from player import Player
from spell import ALL_SPELLS, Spell
from npcs import TRAINING_DUMMY

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

if __name__ == '__main__':
    unittest.main()