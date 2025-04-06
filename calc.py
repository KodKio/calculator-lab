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


def parse_expression(expression):
    expression = expression.replace(" ", "")
    node, index = parse_term(expression, 0)
    if index != len(expression):
        raise ValueError(f"Incomplete or invalid expression at position {index}.")
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
    left, index = parse_exponent(expression, index)
    while index < len(expression) and expression[index] in "*/":
        op = expression[index]
        index += 1
        right, index = parse_exponent(expression, index)
        if op == '*':
            left = Mult(left, right)
        elif op == '/':
            left = Div(left, right)
    return left, index


def parse_exponent(expression, index):
    left, index = parse_primary(expression, index)
    while index < len(expression) and expression[index] == '^':
        index += 1
        right, index = parse_primary(expression, index)
        left = Pow(left, right)
    return left, index


def parse_primary(expression, index):
    if index < len(expression) and expression[index] == '(':
        index += 1
        node, index = parse_term(expression, index)
        if index >= len(expression) or expression[index] != ')':
            raise ValueError("Mismatched parentheses.")
        index += 1
        return node, index

    # Обработка унарного минуса
    if index < len(expression) and expression[index] == '-':
        index += 1
        node, index = parse_primary(expression, index)
        return Minus(Number(0), node), index

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


def evaluate_expression(expression):
    try:
        tree = parse_expression(expression)
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
