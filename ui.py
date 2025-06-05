"""
Tkinter-based UI for the Harry Potter RPG game.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, Dict, Any

class HogwartsUI:
    """Main UI class for the Hogwarts RPG game."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Hogwarts RPG")
        self.root.geometry("1024x768")
        
        # Configure main grid
        self.root.grid_columnconfigure(0, weight=3)  # Game text area
        self.root.grid_columnconfigure(1, weight=1)  # Stats panel
        self.root.grid_rowconfigure(0, weight=1)     # Main content
        self.root.grid_rowconfigure(1, weight=0)     # Control panel
        
        # Create main frames
        self.create_game_text_area()
        self.create_stats_panel()
        self.create_control_panel()
        
        # Initialize callback storage
        self.callbacks: Dict[str, Callable] = {}
    
    def create_game_text_area(self) -> None:
        """Create the left side game text output area."""
        text_frame = ttk.Frame(self.root)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Game text output
        self.game_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD)
        self.game_text.pack(fill=tk.BOTH, expand=True)
        self.game_text.config(state=tk.DISABLED)
    
    def create_stats_panel(self) -> None:
        """Create the right side stats panel."""
        stats_frame = ttk.Frame(self.root)
        stats_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Player info labels
        self.name_label = ttk.Label(stats_frame, text="Name: -")
        self.name_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.house_label = ttk.Label(stats_frame, text="House: -")
        self.house_label.pack(fill=tk.X, padx=5, pady=2)
        
        # Health and mana with progress bars
        health_frame = ttk.Frame(stats_frame)
        health_frame.pack(fill=tk.X, padx=5, pady=2)
        self.health_label = ttk.Label(health_frame, text="Health: -")
        self.health_label.pack(side=tk.LEFT)
        self.health_bar = ttk.Progressbar(health_frame, length=100, mode='determinate')
        self.health_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        mana_frame = ttk.Frame(stats_frame)
        mana_frame.pack(fill=tk.X, padx=5, pady=2)
        self.mana_label = ttk.Label(mana_frame, text="Mana: -")
        self.mana_label.pack(side=tk.LEFT)
        self.mana_bar = ttk.Progressbar(mana_frame, length=100, mode='determinate')
        self.mana_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        self.knowledge_label = ttk.Label(stats_frame, text="Knowledge: -")
        self.knowledge_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.points_label = ttk.Label(stats_frame, text="House Points: -")
        self.points_label.pack(fill=tk.X, padx=5, pady=2)
        
        # Status effects section
        ttk.Label(stats_frame, text="Status Effects:").pack(fill=tk.X, padx=5, pady=2)
        self.status_list = tk.Listbox(stats_frame, height=3)
        self.status_list.pack(fill=tk.X, padx=5, pady=2)
        
        # Spells list
        ttk.Label(stats_frame, text="Known Spells:").pack(fill=tk.X, padx=5, pady=2)
        spells_frame = ttk.Frame(stats_frame)
        spells_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        self.spells_list = tk.Listbox(spells_frame)
        self.spells_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        spells_scrollbar = ttk.Scrollbar(spells_frame, orient=tk.VERTICAL, command=self.spells_list.yview)
        spells_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.spells_list.config(yscrollcommand=spells_scrollbar.set)
    
    def create_control_panel(self) -> None:
        """Create the bottom control panel."""
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Text entry
        self.input_entry = ttk.Entry(control_frame)
        self.input_entry.pack(fill=tk.X, padx=5, pady=5)
        # Bind Enter key to input submission
        self.input_entry.bind('<Return>', lambda event: self._handle_input_submit())
        
        # Buttons frame
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Action buttons
        self.start_button = ttk.Button(buttons_frame, text="Start Game", command=lambda: self._trigger_callback("start_game"))
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        self.explore_button = ttk.Button(buttons_frame, text="Explore Hogwarts", command=lambda: self._trigger_callback("explore"))
        self.explore_button.pack(side=tk.LEFT, padx=2)
        
        self.class_button = ttk.Button(buttons_frame, text="Attend Class", command=lambda: self._trigger_callback("attend_class"))
        self.class_button.pack(side=tk.LEFT, padx=2)
        
        self.duel_button = ttk.Button(buttons_frame, text="Duel NPC", command=lambda: self._trigger_callback("duel"))
        self.duel_button.pack(side=tk.LEFT, padx=2)
        
        self.spellbook_button = ttk.Button(buttons_frame, text="View Spellbook", command=lambda: self._trigger_callback("view_spellbook"))
        self.spellbook_button.pack(side=tk.LEFT, padx=2)
        
        # Initially disable game buttons
        self._set_game_buttons_state(tk.DISABLED)
    
    def _set_game_buttons_state(self, state: str) -> None:
        """Enable or disable game action buttons."""
        for button in [self.explore_button, self.class_button, 
                      self.duel_button, self.spellbook_button]:
            button.config(state=state)
    
    def update_stats(self, stats: Dict[str, Any]) -> None:
        """Update the stats panel with new player information."""
        self.name_label.config(text=f"Name: {stats['Name']}")
        self.house_label.config(text=f"House: {stats['House']}")
        
        # Update health and mana with progress bars
        health, max_health = map(int, stats['Health'].split('/'))
        self.health_label.config(text=f"Health: {stats['Health']}")
        self.health_bar['value'] = (health / max_health) * 100
        
        mana, max_mana = map(int, stats['Mana'].split('/'))
        self.mana_label.config(text=f"Mana: {stats['Mana']}")
        self.mana_bar['value'] = (mana / max_mana) * 100
        
        self.knowledge_label.config(text=f"Knowledge: {stats['Knowledge']}")
        self.points_label.config(text=f"House Points: {stats['House Points']}")
        
        # Update status effects
        self.status_list.delete(0, tk.END)
        if 'Status Effects' in stats:
            for effect in stats['Status Effects']:
                self.status_list.insert(tk.END, effect)
        
        # Update spells list
        self.spells_list.delete(0, tk.END)
        for spell in stats['Known Spells']:
            self.spells_list.insert(tk.END, spell)
    
    def write_to_game_text(self, text: str) -> None:
        """Write text to the game output area."""
        self.game_text.config(state=tk.NORMAL)
        self.game_text.insert(tk.END, text + "\n")
        self.game_text.see(tk.END)
        self.game_text.config(state=tk.DISABLED)
    
    def clear_game_text(self) -> None:
        """Clear the game text area."""
        self.game_text.config(state=tk.NORMAL)
        self.game_text.delete(1.0, tk.END)
        self.game_text.config(state=tk.DISABLED)
    
    def get_input_text(self) -> str:
        """Get text from the input entry and clear it."""
        text = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        return text
    
    def register_callback(self, action: str, callback: Callable) -> None:
        """Register a callback function for a specific action."""
        self.callbacks[action] = callback
    
    def _trigger_callback(self, action: str) -> None:
        """Trigger a registered callback function."""
        if action in self.callbacks:
            self.callbacks[action]()
    
    def start_game_mode(self) -> None:
        """Switch UI to game mode after starting."""
        self.start_button.config(text="New Game")
        self._set_game_buttons_state(tk.NORMAL)
    
    def get_selected_spell(self) -> str:
        """Get the currently selected spell from the spells list."""
        selection = self.spells_list.curselection()
        if selection:
            return self.spells_list.get(selection[0])
        return ""
    
    def _handle_input_submit(self) -> None:
        """Handle input submission when Enter key is pressed."""
        text = self.get_input_text()
        if "submit_text" in self.callbacks and self.callbacks["submit_text"] is not None:
            self.callbacks["submit_text"](text)
        
    def run(self) -> None:
        """Start the UI main loop."""
        self.root.mainloop()