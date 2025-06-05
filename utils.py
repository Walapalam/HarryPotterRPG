"""
Utility functions for the Harry Potter RPG game.
Contains helper functions like the sorting hat quiz and random events.
"""
import random
from typing import Dict, List, Tuple


def clear_screen() -> None:
    """Clear the console screen."""
    print("\n" * 50)


def get_valid_input(prompt: str, valid_options: List[str]) -> str:
    """
    Get user input and validate it against a list of valid options.
    
    Args:
        prompt: The prompt to show the user
        valid_options: List of valid input options
        
    Returns:
        str: The validated user input
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please choose from: {', '.join(valid_options)}")


def sorting_hat_quiz() -> str:
    """
    Run the sorting hat quiz to determine the player's house.
    
    Returns:
        str: The chosen house name
    """
    # Questions and their house affinities
    questions = [
        {
            "question": "Which quality do you value most?",
            "options": {
                "1": ("Courage", "gryffindor"),
                "2": ("Ambition", "slytherin"),
                "3": ("Loyalty", "hufflepuff"),
                "4": ("Wisdom", "ravenclaw")
            }
        },
        {
            "question": "Which pet would you bring to Hogwarts?",
            "options": {
                "1": ("Lion", "gryffindor"),
                "2": ("Snake", "slytherin"),
                "3": ("Badger", "hufflepuff"),
                "4": ("Eagle", "ravenclaw")
            }
        },
        {
            "question": "How would you like to be remembered?",
            "options": {
                "1": ("The Bold", "gryffindor"),
                "2": ("The Great", "slytherin"),
                "3": ("The Good", "hufflepuff"),
                "4": ("The Wise", "ravenclaw")
            }
        }
    ]
    
    # Track house points
    house_points = {
        "gryffindor": 0,
        "slytherin": 0,
        "hufflepuff": 0,
        "ravenclaw": 0
    }
    
    print("\nThe Sorting Hat will now determine your house!")
    
    # Ask each question
    for q in questions:
        print(f"\n{q['question']}")
        for num, (option, _) in q['options'].items():
            print(f"{num}. {option}")
        
        # Get valid input
        choice = get_valid_input("Your choice (1-4): ", list(q['options'].keys()))
        
        # Award point to chosen house
        _, house = q['options'][choice]
        house_points[house] += 1
    
    # Find house with most points (random tiebreaker)
    max_points = max(house_points.values())
    chosen_house = random.choice([
        house for house, points in house_points.items()
        if points == max_points
    ])
    
    return chosen_house.capitalize()


def generate_random_event() -> Tuple[str, int]:
    """
    Generate a random event for exploration.
    
    Returns:
        Tuple[str, int]: (event description, house points earned/lost)
    """
    events = [
        ("You found a secret passage! +10 points", 10),
        ("You helped a lost first-year student. +5 points", 5),
        ("You discovered a magical artifact! +15 points", 15),
        ("You were caught out after curfew! -10 points", -10),
        ("You successfully answered a riddle from a portrait. +5 points", 5),
        ("You found and returned a lost wand. +10 points", 10),
        ("You accidentally set off a dungbomb! -5 points", -5),
        ("You helped Hagrid with magical creatures. +15 points", 15)
    ]
    
    return random.choice(events)