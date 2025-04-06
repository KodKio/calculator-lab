import unittest
import math
from calc import *

class TestParser(unittest.TestCase):

    def test_single_number(self):
        self.assertEqual(parse_expression("42").evaluate(), 42)

    def test_scientific_notation(self):
        self.assertEqual(parse_expression("1.25e+09").evaluate(), 1.25e+09)

    def test_simple_addition(self):
        self.assertEqual(parse_expression("1+1").evaluate(), 2)

    def test_simple_subtraction(self):
        self.assertEqual(parse_expression("5-3").evaluate(), 2)

    def test_simple_multiplication(self):
        self.assertEqual(parse_expression("4*2").evaluate(), 8)

    def test_simple_division(self):
        self.assertEqual(parse_expression("8/2").evaluate(), 4)

    def test_exponentiation(self):
        self.assertEqual(parse_expression("3^4").evaluate(), 81)

    def test_combined_operations(self):
        self.assertEqual(parse_expression("2+3*4").evaluate(), 14)
        self.assertEqual(parse_expression("2*3+4").evaluate(), 10)

    def test_operator_precedence(self):
        self.assertEqual(parse_expression("2+3*4-5/5").evaluate(), 13)
        self.assertEqual(parse_expression("10/2+3*2").evaluate(), 11)

    def test_parentheses(self):
        self.assertAlmostEqual(parse_expression("1+2/(3+4)").evaluate(), 1.2857142857142856)

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            parse_expression("2+*3")

    def test_invalid_characters(self):
        with self.assertRaises(ValueError):
            parse_expression("2+3a")

    def test_unsupported_operations(self):
        with self.assertRaises(ValueError):
            parse_expression("1+4j")

    def test_incomplete_expression(self):
        with self.assertRaises(ValueError):
            parse_expression("2+")
        with self.assertRaises(ValueError):
            parse_expression("3*")

    def test_invalid_symbols(self):
        with self.assertRaises(ValueError):
            parse_expression("2+3@5")
        with self.assertRaises(ValueError):
            parse_expression("1+2#3")

    def test_executable_code_attempt(self):
        with self.assertRaises(ValueError):
            parse_expression("0; import os; os.system('echo hello')")

class TestEvaluator(unittest.TestCase):

    def test_plus(self):
        self.assertEqual(Plus(Number(2), Number(2)).evaluate(), 4)

    def test_minus(self):
        self.assertEqual(Minus(Number(5), Number(3)).evaluate(), 2)

    def test_mult(self):
        self.assertEqual(Mult(Number(4), Number(2)).evaluate(), 8)

    def test_div(self):
        self.assertEqual(Div(Number(8), Number(2)).evaluate(), 4)

    def test_div_by_zero(self):
        expr = Div(Number(1), Number(0))
        with self.assertRaises(ZeroDivisionError):
            expr.evaluate()

    def test_arithmetic_overflow(self):
        result = Div(Number(1e300), Number(1e-300)).evaluate()
        self.assertTrue(math.isinf(result), "Expected result to be infinity due to overflow")

class TestIntegration(unittest.TestCase):

    def test_integration(self):
        self.assertAlmostEqual(evaluate_expression("3.375e+09^(1/3)"), 1500)

    def test_integration_zero_division(self):
        result = evaluate_expression("1/0")
        self.assertEqual(result, "Error during evaluation: Division by zero.")

    def test_integration_parser_error(self):
        result = evaluate_expression("1/")
        self.assertEqual(result, "Parser error: Invalid number at position 2.")

if __name__ == "__main__":
    unittest.main()