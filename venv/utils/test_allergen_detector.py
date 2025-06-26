import unittest
import sys
import os
from .allergen_detector import detect_allergens_spacy

# Add parent directory to sys.path to import allergen_detector
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAllergenDetection(unittest.TestCase):
    def setUp(self):
        self.allergen_list = ["milk", "peanut", "soy lecithin", "gluten"]

    def test_phrase_matcher(self):
        result = detect_allergens_spacy("Contains soy lecithin and milk.", self.allergen_list)
        self.assertIn("soy lecithin", result)
        self.assertIn("milk", result)

    def test_token_similarity(self):
        result = detect_allergens_spacy("May include milkfat or peanutbutter.", self.allergen_list)
        self.assertIn("milk", result)
        self.assertIn("peanut", result)

    def test_lemma_match(self):
        result = detect_allergens_spacy("Includes milks, peanuts, and glutenous grains.", self.allergen_list)
        self.assertIn("milk", result)
        self.assertIn("peanut", result)

    def test_ner(self):
        result = detect_allergens_spacy("Made by Peanut Corp and contains gluten.", self.allergen_list)
        self.assertIn("peanut", result)
        self.assertIn("gluten", result)

if __name__ == "__main__":
    unittest.main()
