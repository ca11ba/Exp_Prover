# main.py
from parser import Parser

if __name__ == "__main__":
    expressions = [
        "(A > C) > ((B > C) > ((A | B) > C))",
        "A = C > (B = C)",
        "(!A * B) | C",
        "A + B * !C = D > E"
    ]
    
    for expr in expressions:
        try:
            parser = Parser(expr)
            expression_tree = parser.parse()
            print(f"Выражение: {expr}")
            print(f"Дерево выражений: {expression_tree.to_string()}\n")
        except ValueError as e:
            print(f"Ошибка при парсинге выражения '{expr}': {e}\n")
