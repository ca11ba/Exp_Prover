# main.py
from parser import Parser

if __name__ == "__main__":
    expressions = [
        "A * B > A",
        "A * B > B",
        "A > (B > (A * B))",
        "A > (A|B)",
        "B>(A|B)",
        "(A>C)>((B>C)>((A|B)>C))",
        " !A>(A>B)",
        "A|!A",
        "A+B",
        "A=B>C",
        "A=B"
    ]
    
    for expr in expressions:
        try:
            parser = Parser(expr)
            expression_tree = parser.parse()
            print(f"Выражение: {expr}")
            print(f"Преобразованное выражение: {expression_tree.to_string()}\n")
        except ValueError as e:
            print(f"Ошибка при парсинге выражения '{expr}': {e}\n")
