import unittest
import math
from calc import *
import subprocess
import time


class TestCalculatorPerformance(unittest.TestCase):

    def run_calc(self, expression):
        """Helper function to run the calc command with specified expression."""
        start_time = time.time()
        result = subprocess.run(['python', 'calc.py', expression], capture_output=True, text=True)
        end_time = time.time()
        duration = end_time - start_time
        return result.stdout.strip(), result.returncode, duration

    def test_long_addition(self):
        expression = " + ".join(["1"] * 250)
        output, returncode, duration = self.run_calc(expression)
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertEqual(result_value, 250.0)
        self.assertLessEqual(duration, 0.3)

    def test_long_addition_with_error(self):
        expression = " + ".join(["1"] * 250) + " +"
        output, returncode, duration = self.run_calc(expression)
        self.assertNotEqual(returncode, 0)
        self.assertIn("error", output.lower())
        self.assertLessEqual(duration, 0.3)

    def test_large_numbers(self):
        expression = "+".join(["1e100"] * 4)
        output, returncode, duration = self.run_calc(expression)
        self.assertEqual(returncode, 0)
        self.assertEqual(output.split(":")[1].strip(), "4e+100")
        self.assertLessEqual(duration, 0.3)

    def test_large_exponent(self):
        expression = "1 ^ 36893488147419103232"
        output, returncode, duration = self.run_calc(expression)
        print(output)
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertEqual(result_value, 1.0)  # Приведение к float для сравнения

    def test_very_long_expression(self):
        expression = "+".join(["1"] * 900)
        output, returncode, duration = self.run_calc(expression)
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertEqual(result_value, 900.0)
        self.assertLessEqual(duration, 0.5)


class TestCalculatorCLI(unittest.TestCase):

    def run_calc(self, args):
        """Helper function to run the calc command with specified arguments."""
        result = subprocess.run(['python', 'calc.py'] + args, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode

    def test_sin_degree(self):
        output, returncode = self.run_calc(['--angle-unit=degree', 'sin(90)'])
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertAlmostEqual(result_value, 1)

    def test_sin_radian(self):
        output, returncode = self.run_calc(['--angle-unit=radian', 'sin(pi/2)'])
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertAlmostEqual(result_value, 1)

    def test_sin_default(self):
        output, returncode = self.run_calc(['sin(pi/2)'])
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertAlmostEqual(result_value, 1)

    def test_sqrt_expression(self):
        output, returncode = self.run_calc(['sqrt(2^2 * 5 + 1)'])
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertAlmostEqual(result_value, 4.58257569495584)

    def test_exp_ln(self):
        output, returncode = self.run_calc(['exp(ln(2))'])
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertAlmostEqual(result_value, 2)

    def test_ln_exp(self):
        output, returncode = self.run_calc(['ln(exp(2))'])
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertAlmostEqual(result_value, 2)

    def test_ln_e_squared(self):
        output, returncode = self.run_calc(['ln(e^2)'])
        self.assertEqual(returncode, 0)
        result_value = float(output.split(":")[1].strip())
        self.assertAlmostEqual(result_value, 2)


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

    def test_parse_functions(self):
        node = parse_expression("sqrt(4)")
        self.assertIsInstance(node, Sqrt)
        self.assertEqual(node.evaluate(), 2)

        node = parse_expression("ln(e)")
        self.assertIsInstance(node, Ln)
        self.assertAlmostEqual(node.evaluate(), 1)

        node = parse_expression("exp(1)")
        self.assertIsInstance(node, Exp)
        self.assertAlmostEqual(node.evaluate(), math.e)

    def test_parse_constants(self):
        node = parse_expression("pi")
        self.assertIsInstance(node, Pi)
        self.assertAlmostEqual(node.evaluate(), math.pi)

        node = parse_expression("e")
        self.assertIsInstance(node, E)
        self.assertAlmostEqual(node.evaluate(), math.e)

    def test_parse_trigonometric_functions(self):
        node = parse_expression("sin(pi/2)")
        self.assertIsInstance(node, Sin)
        self.assertAlmostEqual(node.evaluate(), 1)

        node = parse_expression("cos(0)")
        self.assertIsInstance(node, Cos)
        self.assertAlmostEqual(node.evaluate(), 1)

        node = parse_expression("tg(pi/4)")
        self.assertIsInstance(node, Tg)
        self.assertAlmostEqual(node.evaluate(), 1)

        node = parse_expression("ctg(pi/4)")
        self.assertIsInstance(node, Ctg)
        self.assertAlmostEqual(node.evaluate(), 1)


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

    def test_evaluate_sqrt(self):
        expr = Sqrt(Number(4))
        self.assertEqual(expr.evaluate(), 2)

    def test_evaluate_ln(self):
        expr = Ln(E())
        self.assertAlmostEqual(expr.evaluate(), 1)

    def test_evaluate_exp(self):
        expr = Exp(Number(1))
        self.assertAlmostEqual(expr.evaluate(), math.e)

    def test_evaluate_sin(self):
        expr = Sin(Pi())
        self.assertAlmostEqual(expr.evaluate(), 0)

    def test_evaluate_cos(self):
        expr = Cos(Number(0))
        self.assertAlmostEqual(expr.evaluate(), 1)

    def test_evaluate_tg(self):
        expr = Tg(Pi())
        self.assertAlmostEqual(expr.evaluate(), 0)

    def test_evaluate_ctg(self):
        expr = Ctg(Div(Pi(), Number(2)))
        self.assertAlmostEqual(expr.evaluate(), 0)


class TestIntegration(unittest.TestCase):

    def test_integration(self):
        self.assertAlmostEqual(evaluate_expression("3.375e+09^(1/3)"), 1500)

    def test_integration_zero_division(self):
        result = evaluate_expression("1/0")
        self.assertEqual(result, "Error during evaluation: Division by zero.")

    def test_integration_parser_error(self):
        result = evaluate_expression("1/")
        self.assertEqual(result, "Parser error: Invalid number at position 2.")

    def test_functions(self):
        self.assertAlmostEqual(evaluate_expression("sqrt(ln(e))"), 1)
        self.assertAlmostEqual(evaluate_expression("exp(ln(2))"), 2)
        self.assertAlmostEqual(evaluate_expression("ln(exp(2))"), 2)
        self.assertAlmostEqual(evaluate_expression("ln(e^2)"), 2)

    def test_trigonometric_functions_radian(self):
        self.assertAlmostEqual(evaluate_expression("sin(pi/2)"), 1)
        self.assertAlmostEqual(evaluate_expression("cos(0)"), 1)
        self.assertAlmostEqual(evaluate_expression("tg(pi/4)"), 1)
        self.assertAlmostEqual(evaluate_expression("ctg(pi/4)"), 1)

    def test_trigonometric_functions_degree(self):
        self.assertAlmostEqual(evaluate_expression("sin(90)", angle_unit='degree'), 1)
        self.assertAlmostEqual(evaluate_expression("cos(0)", angle_unit='degree'), 1)
        self.assertAlmostEqual(evaluate_expression("tg(45)", angle_unit='degree'), 1)
        self.assertAlmostEqual(evaluate_expression("ctg(45)", angle_unit='degree'), 1)


if __name__ == "__main__":
    unittest.main()
