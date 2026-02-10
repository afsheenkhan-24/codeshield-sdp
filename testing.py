import unittest
from analysis import calculate_complexity

class TestComplexity(unittest.TestCase):

    def test_script_1(self):
        code = "print('Hello')"
        self.assertEqual(calculate_complexity(code), 1)

    def test_armstrong_logic(self):
        code = """
                while n > 0:
                    n //= 10
                if total == num:
                    print('Match')
"""
        self.assertEqual(calculate_complexity(code), 3)

    def test_high_complexity(self):
        code = "if 1>2: \n if 2>3: \n if 3>4: \n while True:"
        self.assertEqual(calculate_complexity(code), 5)

if __name__ == "__main__":
    unittest.main()