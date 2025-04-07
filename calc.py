import math


class Node:
    def evaluate(self):
        raise NotImplementedError("This method should be implemented by subclasses.")


class Number(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class Plus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()


class Minus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()


class Mult(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()


class Div(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        right_value = self.right.evaluate()
        if right_value == 0:
            raise ZeroDivisionError("Division by zero.")
        return self.left.evaluate() / right_value


class Pow(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        return self.left.evaluate() ** self.right.evaluate()


class Sqrt(Node):
    def __init__(self, operand):
        self.operand = operand

    def evaluate(self):
        return math.sqrt(self.operand.evaluate())


class Sin(Node):
    def __init__(self, operand, angle_unit='radian'):
        self.operand = operand
        self.angle_unit = angle_unit

    def evaluate(self):
        angle = self.operand.evaluate()
        if self.angle_unit == 'degree':
            angle = math.radians(angle)
        return math.sin(angle)


class Cos(Node):
    def __init__(self, operand, angle_unit='radian'):
        self.operand = operand
        self.angle_unit = angle_unit

    def evaluate(self):
        angle = self.operand.evaluate()
        if self.angle_unit == 'degree':
            angle = math.radians(angle)
        return math.cos(angle)


class Tg(Node):
    def __init__(self, operand, angle_unit='radian'):
        self.operand = operand
        self.angle_unit = angle_unit

    def evaluate(self):
        angle = self.operand.evaluate()
        if self.angle_unit == 'degree':
            angle = math.radians(angle)
        return math.tan(angle)


class Ctg(Node):
    def __init__(self, operand, angle_unit='radian'):
        self.operand = operand
        self.angle_unit = angle_unit

    def evaluate(self):
        angle = self.operand.evaluate()
        if self.angle_unit == 'degree':
            angle = math.radians(angle)
        return 1 / math.tan(angle)


class Ln(Node):
    def __init__(self, operand):
        self.operand = operand

    def evaluate(self):
        return math.log(self.operand.evaluate())


class Exp(Node):
    def __init__(self, operand):
        self.operand = operand

    def evaluate(self):
        return math.exp(self.operand.evaluate())


class Pi(Node):
    def evaluate(self):
        return math.pi


class E(Node):
    def evaluate(self):
        return math.e


def parse_expression(expression, angle_unit='radian'):
    expression = expression.replace(" ", "")
    node, index = parse_term(expression, 0, angle_unit)
    if index != len(expression):
        raise ValueError(f"Incomplete or invalid expression at position {index}.")
    return node


def parse_term(expression, index, angle_unit):
    left, index = parse_factor(expression, index, angle_unit)
    while index < len(expression) and expression[index] in "+-":
        op = expression[index]
        index += 1
        right, index = parse_factor(expression, index, angle_unit)
        if op == '+':
            left = Plus(left, right)
        elif op == '-':
            left = Minus(left, right)
    return left, index


def parse_factor(expression, index, angle_unit):
    left, index = parse_exponent(expression, index, angle_unit)
    while index < len(expression) and expression[index] in "*/":
        op = expression[index]
        index += 1
        right, index = parse_exponent(expression, index, angle_unit)
        if op == '*':
            left = Mult(left, right)
        elif op == '/':
            left = Div(left, right)
    return left, index


def parse_exponent(expression, index, angle_unit):
    left, index = parse_primary(expression, index, angle_unit)
    while index < len(expression) and expression[index] == '^':
        index += 1
        right, index = parse_primary(expression, index, angle_unit)
        left = Pow(left, right)
    return left, index


def parse_primary(expression, index, angle_unit):
    if index < len(expression) and expression[index] == '(':
        index += 1
        node, index = parse_term(expression, index, angle_unit)
        if index >= len(expression) or expression[index] != ')':
            raise ValueError("Mismatched parentheses.")
        index += 1
        return node, index

    if index < len(expression):
        if expression.startswith("sqrt", index):
            index += 4
            node, index = parse_primary(expression, index, angle_unit)
            return Sqrt(node), index
        elif expression.startswith("sin", index):
            index += 3
            node, index = parse_primary(expression, index, angle_unit)
            return Sin(node, angle_unit), index
        elif expression.startswith("cos", index):
            index += 3
            node, index = parse_primary(expression, index, angle_unit)
            return Cos(node, angle_unit), index
        elif expression.startswith("tg", index):
            index += 2
            node, index = parse_primary(expression, index, angle_unit)
            return Tg(node, angle_unit), index
        elif expression.startswith("ctg", index):
            index += 3
            node, index = parse_primary(expression, index, angle_unit)
            return Ctg(node, angle_unit), index
        elif expression.startswith("ln", index):
            index += 2
            node, index = parse_primary(expression, index, angle_unit)
            return Ln(node), index
        elif expression.startswith("exp", index):
            index += 3
            node, index = parse_primary(expression, index, angle_unit)
            return Exp(node), index
        elif expression.startswith("pi", index):
            index += 2
            return Pi(), index
        elif expression.startswith("e", index):
            index += 1
            return E(), index

    return parse_number(expression, index)


def parse_number(expression, index):
    start_index = index
    has_decimal = False
    has_exponent = False

    while index < len(expression):
        char = expression[index]
        if char.isdigit():
            index += 1
        elif char == '.' and not has_decimal:
            has_decimal = True
            index += 1
        elif (char == 'e' or char == 'E') and not has_exponent:
            has_exponent = True
            index += 1
            # После 'e' или 'E' может следовать знак '+' или '-'
            if index < len(expression) and expression[index] in '+-':
                index += 1
        else:
            break

    if start_index == index:
        raise ValueError(f"Invalid number at position {index}.")

    try:
        value = float(expression[start_index:index])
    except ValueError:
        raise ValueError(f"Invalid number format at position {start_index}.")

    return Number(value), index


def evaluate_expression(expression, angle_unit='radian'):
    try:
        tree = parse_expression(expression, angle_unit)
        return tree.evaluate()
    except ZeroDivisionError as e:
        return f"Error during evaluation: {e}"
    except ValueError as e:
        return f"Parser error: {e}"


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python calculator.py '<expression>'")
        sys.exit(1)

    expression = sys.argv[1]
    result = evaluate_expression(expression)

    if result is not None:
        print(f"Result: {result}")
    else:
        sys.exit(1)
