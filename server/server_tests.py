"""Unit tests for palindrome server"""
import unittest
from palinchecker_server import is_palindrome

class TestPalindromes(unittest.TestCase):
    """Tests the is_palindrome() function with various values"""
    def test_lower(self):
        """tests valid lowercase palindrome"""
        self.assertTrue(is_palindrome("racecar"))
    def test_upper(self):
        """tests valid uppercase palindrome"""
        self.assertTrue(is_palindrome("ABBA"))
    def test_bad(self):
        """tests a non-palindrome"""
        self.assertFalse(is_palindrome("Victory"))
    def test_singlechar(self):
        """Tests a single character"""
        self.assertTrue(is_palindrome("X"))
    def test_mixed_case(self):
        """Tests a mixed case palindrome"""
        self.assertTrue(is_palindrome("evE"))

if __name__ == '__main__':
    unittest.main()
