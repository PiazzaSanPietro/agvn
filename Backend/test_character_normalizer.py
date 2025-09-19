"""
Unit Tests for Character Name Normalization

This module contains comprehensive unit tests for the character_normalizer.py module.
Tests cover all character mappings, edge cases, and safety features.

Run with: python -m pytest test_character_normalizer.py -v
Or: python test_character_normalizer.py
"""

import unittest
from tool.character_normalizer import (
    normalize_character_name,
    get_all_standardized_characters,
    get_character_variations
)


class TestCharacterNormalization(unittest.TestCase):
    """Test cases for character name normalization functionality."""
    
    def test_seraphina_variations(self):
        """Test all Seraphina character name variations."""
        test_cases = [
            ("Princess Seraphina Elara Aethelgard", "Seraphina"),
            ("Princess Seraphina", "Seraphina"),
            ("princess seraphina", "Seraphina"),  # Case insensitive
            ("PRINCESS SERAPHINA", "Seraphina"),  # All caps
            ("Seraphina", "Seraphina"),
            ("seraphina", "Seraphina"),  # Lowercase
            ("Saintess", "Seraphina"),
            ("saintess", "Seraphina"),  # Case insensitive
            ("세라피나", "Seraphina"),  # Korean
            ("Saintess of the White Lily", "Seraphina"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_character_name(input_name)
                self.assertEqual(result, expected, 
                    f"Failed to normalize '{input_name}' to '{expected}', got '{result}'")
    
    def test_valerius_variations(self):
        """Test all Valerius character name variations."""
        test_cases = [
            ("Captain Valerius Arkright", "Valerius"),
            ("Captain Valerius", "Valerius"),
            ("captain valerius", "Valerius"),  # Case insensitive
            ("Valerius", "Valerius"),
            ("valerius", "Valerius"),  # Lowercase
            ("Lion of Aethelgard", "Valerius"),
            ("발레리우스", "Valerius"),  # Korean
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_character_name(input_name)
                self.assertEqual(result, expected)
    
    def test_lyra_variations(self):
        """Test all Lyra character name variations."""
        test_cases = [
            ("Lyra Willowshade", "Lyra"),
            ("lyra willowshade", "Lyra"),  # Case insensitive
            ("Lyra", "Lyra"),
            ("lyra", "Lyra"),  # Lowercase
            ("Sage of the Sunstone Spire", "Lyra"),
            ("리라", "Lyra"),  # Korean
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_character_name(input_name)
                self.assertEqual(result, expected)
    
    def test_deadpool_variations(self):
        """Test all Deadpool character name variations."""
        test_cases = [
            ("Deadpool", "Deadpool"),
            ("deadpool", "Deadpool"),  # Case insensitive
            ("DEADPOOL", "Deadpool"),  # All caps
            ("Wade", "Deadpool"),
            ("wade", "Deadpool"),  # Case insensitive
            ("Merc with a Mouth", "Deadpool"),
            ("데드풀", "Deadpool"),  # Korean
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_character_name(input_name)
                self.assertEqual(result, expected)
    
    def test_antagonist_variations(self):
        """Test all antagonist character name variations."""
        test_cases = [
            # Demon Lord
            ("Demon Lord of Miasma", "Demon Lord"),
            ("demon lord", "Demon Lord"),
            ("데몬로드", "Demon Lord"),
            
            # Vorlag
            ("General Vorlag the Annihilator", "Vorlag"),
            ("General Vorlag", "Vorlag"),
            ("Vorlag the Annihilator", "Vorlag"),
            ("vorlag", "Vorlag"),
            ("보를라그", "Vorlag"),
            
            # Lilith
            ("Duchess Lilith the Puppeteer", "Lilith"),
            ("Duchess Lilith", "Lilith"),
            ("Lilith the Puppeteer", "Lilith"),
            ("lilith", "Lilith"),
            ("릴리스", "Lilith"),
            
            # Volkov
            ("Count Volkov the Blighted Knight", "Volkov"),
            ("Count Volkov", "Volkov"),
            ("Volkov the Blighted Knight", "Volkov"),
            ("volkov", "Volkov"),
            ("볼코프", "Volkov"),
            
            # Zarthus
            ("Archmage Zarthus the Void-Caller", "Zarthus"),
            ("Archmage Zarthus", "Zarthus"),
            ("Zarthus the Void-Caller", "Zarthus"),
            ("zarthus", "Zarthus"),
            ("자르투스", "Zarthus"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_character_name(input_name)
                self.assertEqual(result, expected)
    
    def test_narrator_variations(self):
        """Test narrator character name variations."""
        test_cases = [
            ("Narrator", "Narrator"),
            ("narrator", "Narrator"),  # Case insensitive
            ("내레이터", "Narrator"),  # Korean
            ("System", "Narrator"),
            ("system", "Narrator"),  # Case insensitive
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_character_name(input_name)
                self.assertEqual(result, expected)
    
    def test_unknown_character_preservation(self):
        """Test that unknown characters are preserved unchanged."""
        unknown_names = [
            "Unknown Character",
            "Random Name",
            "새로운캐릭터",  # Korean unknown
            "Character with Special !@# Symbols",
            "   Whitespace Padded   ",
            "123 Numeric Character",
        ]
        
        for unknown_name in unknown_names:
            with self.subTest(unknown_name=unknown_name):
                result = normalize_character_name(unknown_name)
                self.assertEqual(result, unknown_name, 
                    f"Unknown character '{unknown_name}' was not preserved")
    
    def test_edge_cases(self):
        """Test edge cases and invalid inputs."""
        test_cases = [
            (None, None),  # None input
            ("", ""),  # Empty string
            ("   ", "   "),  # Whitespace only
            (123, 123),  # Non-string input
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = normalize_character_name(input_val)
                self.assertEqual(result, expected)
    
    def test_case_insensitive_matching(self):
        """Test that matching is case insensitive."""
        test_cases = [
            ("SERAPHINA", "Seraphina"),
            ("seraphina", "Seraphina"),
            ("SeRaPhInA", "Seraphina"),
            ("DEADPOOL", "Deadpool"),
            ("DeAdPoOl", "Deadpool"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_character_name(input_name)
                self.assertEqual(result, expected)
    
    def test_substring_matching(self):
        """Test partial/substring matching functionality."""
        test_cases = [
            ("Something Princess Seraphina Something", "Seraphina"),
            ("The Great Captain Valerius", "Valerius"),
            ("Lady Lyra of the Forest", "Lyra"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_character_name(input_name)
                self.assertEqual(result, expected)
    
    def test_get_all_standardized_characters(self):
        """Test getting list of all standardized character names."""
        characters = get_all_standardized_characters()
        expected_characters = {
            "Seraphina", "Valerius", "Lyra", "Deadpool", 
            "Demon Lord", "Vorlag", "Lilith", "Volkov", "Zarthus", "Narrator"
        }
        
        self.assertIsInstance(characters, list)
        character_set = set(characters)
        
        # Check that all expected characters are present
        for expected_char in expected_characters:
            self.assertIn(expected_char, character_set, 
                f"Expected character '{expected_char}' not found in standardized list")
    
    def test_get_character_variations(self):
        """Test getting variations for a specific character."""
        seraphina_variations = get_character_variations("Seraphina")
        self.assertIsInstance(seraphina_variations, list)
        self.assertGreater(len(seraphina_variations), 0)
        
        # Check that common variations are included
        expected_variations = ["seraphina", "princess seraphina", "세라피나"]
        for variation in expected_variations:
            self.assertIn(variation, seraphina_variations, 
                f"Expected variation '{variation}' not found for Seraphina")
        
        # Test non-existent character
        unknown_variations = get_character_variations("Unknown Character")
        self.assertEqual(unknown_variations, [])


def run_basic_tests():
    """Run basic functionality tests for manual verification."""
    print("=== Character Normalizer Basic Tests ===")
    
    test_cases = [
        # Basic functionality
        ("Seraphina", "Seraphina"),
        ("Princess Seraphina", "Seraphina"),
        ("세라피나", "Seraphina"),
        ("DEADPOOL", "Deadpool"),
        ("Unknown Character", "Unknown Character"),
        
        # Case sensitivity
        ("seraphina", "Seraphina"),
        ("captain valerius", "Valerius"),
        
        # Edge cases
        (None, None),
        ("", ""),
    ]
    
    print("Testing normalize_character_name function:")
    for input_name, expected in test_cases:
        result = normalize_character_name(input_name)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {status} '{input_name}' -> '{result}' (expected: '{expected}')")
    
    print(f"\nStandardized characters: {get_all_standardized_characters()}")
    print(f"Seraphina variations: {get_character_variations('Seraphina')}")
    
    print("\n=== Tests Complete ===")


if __name__ == "__main__":
    # Run basic tests for manual verification
    run_basic_tests()
    
    print("\nRunning full unittest suite...")
    unittest.main(verbosity=2)