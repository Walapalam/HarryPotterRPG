"""
Unit tests for the Hogwarts RPG UI system.
"""
import unittest
import tkinter as tk
from ui import HogwartsUI

class TestHogwartsUI(unittest.TestCase):
    """Test cases for the HogwartsUI class."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.root = tk.Tk()
        self.ui = HogwartsUI(self.root)
    
    def tearDown(self):
        """Clean up after each test."""
        self.root.destroy()
    
    def test_ui_initialization(self):
        """Test that UI components are properly initialized."""
        # Test main window properties
        self.assertEqual(self.root.title(), "Hogwarts RPG")
        
        # Test that main components exist
        self.assertTrue(hasattr(self.ui, 'game_text'))
        self.assertTrue(hasattr(self.ui, 'spells_list'))
        self.assertTrue(hasattr(self.ui, 'input_entry'))
        
        # Test initial labels
        self.assertEqual(self.ui.name_label['text'], "Name: -")
        self.assertEqual(self.ui.house_label['text'], "House: -")
        self.assertEqual(self.ui.health_label['text'], "Health: -")
        self.assertEqual(self.ui.mana_label['text'], "Mana: -")
    
    def test_update_stats(self):
        """Test updating player stats in the UI."""
        test_stats = {
            "Name": "Harry",
            "House": "Gryffindor",
            "Health": "100/100",
            "Mana": "100/100",
            "Knowledge": 10,
            "House Points": 50,
            "Known Spells": ["Lumos", "Wingardium Leviosa"],
            "Inventory": ["Wand", "Textbooks"]
        }
        
        self.ui.update_stats(test_stats)
        
        self.assertEqual(self.ui.name_label['text'], "Name: Harry")
        self.assertEqual(self.ui.house_label['text'], "House: Gryffindor")
        self.assertEqual(self.ui.health_label['text'], "Health: 100/100")
        self.assertEqual(self.ui.mana_label['text'], "Mana: 100/100")
        
        # Test spells list
        spells = list(self.ui.spells_list.get(0, tk.END))
        self.assertEqual(spells, ["Lumos", "Wingardium Leviosa"])
    
    def test_game_text_operations(self):
        """Test game text area operations."""
        test_message = "Welcome to Hogwarts!"
        self.ui.write_to_game_text(test_message)
        
        # Get text content (excluding newline)
        text_content = self.ui.game_text.get("1.0", tk.END).strip()
        self.assertEqual(text_content, test_message)
        
        # Test clear operation
        self.ui.clear_game_text()
        text_content = self.ui.game_text.get("1.0", tk.END).strip()
        self.assertEqual(text_content, "")
    
    def test_spell_selection(self):
        """Test spell selection functionality."""
        # Add some test spells
        test_spells = ["Lumos", "Wingardium Leviosa"]
        for spell in test_spells:
            self.ui.spells_list.insert(tk.END, spell)
        
        # Initially no selection
        self.assertEqual(self.ui.get_selected_spell(), "")
        
        # Simulate selection
        self.ui.spells_list.selection_set(0)
        self.assertEqual(self.ui.get_selected_spell(), "Lumos")
    
    def test_input_entry_submit(self):
        """Test input entry submission with Enter key."""
        # Set up a test callback
        submitted_text = []
        def test_callback(text):
            submitted_text.append(text)
        
        self.ui.register_callback("submit_text", test_callback)
        
        # Insert test text and simulate Enter key press
        test_text = "Hello Hogwarts!"
        self.ui.input_entry.insert(0, test_text)
        self.ui.input_entry.event_generate('<Return>')
        
        # Verify callback was triggered with correct text
        self.root.update()  # Process events
        self.assertEqual(submitted_text[0], test_text)
        # Verify input field was cleared
        self.assertEqual(self.ui.input_entry.get(), "")

if __name__ == '__main__':
    unittest.main()