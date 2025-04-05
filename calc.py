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


def parse_expression(expression):
    expression = expression.replace(" ", "")

    # Проверка на допустимые символы
    allowed_chars = set("0123456789+-*/().")
    if not all(char in allowed_chars for char in expression):
        raise ValueError("Expression contains invalid characters.")

    # Проверка на неподдерживаемые операции
    if any(char in expression for char in "^j"):
        raise ValueError("Unsupported operation or character in expression.")

    node, index = parse_term(expression, 0)

    if index != len(expression):
        raise ValueError("Incomplete or invalid expression.")

    return node


def parse_term(expression, index):
    left, index = parse_factor(expression, index)
    while index < len(expression) and expression[index] in "+-":
        op = expression[index]
        index += 1
        # Проверка на наличие операнда после оператора
        right, index = parse_factor(expression, index)
        if op == '+':
            left = Plus(left, right)
        elif op == '-':
            left = Minus(left, right)
    return left, index


def parse_factor(expression, index):
    left, index = parse_number(expression, index)
    while index < len(expression) and expression[index] in "*/":
        op = expression[index]
        index += 1
        # Проверка на наличие операнда после оператора
        right, index = parse_number(expression, index)
        if op == '*':
            left = Mult(left, right)
        elif op == '/':
            left = Div(left, right)
    return left, index


def parse_number(expression, index):
    start_index = index
    while index < len(expression) and (expression[index].isdigit() or expression[index] == '.'):
        index += 1
    if start_index == index:
        raise ValueError("Invalid number at position {}".format(index))
    return Number(float(expression[start_index:index])), index


def evaluate_expression(expression):
    try:
        tree = parse_expression(expression)
        return tree.evaluate()
    except Exception as e:
        print(type(e))
        print(f"Error: {e}")
        return None


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
