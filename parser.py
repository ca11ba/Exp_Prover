import re
from typing import List, Union
from expressions import *

class Parser:
    TOKEN_REGEX = re.compile(r'\s*(?:(\()|(\))|(\|)|(\*)|(!)|(\+)|(>)|(=)|([A-Za-z]))')

    def __init__(self, expression: str):
        self.expression = expression
        self.tokens = self.tokenize(expression)
        self.pos = 0

    def tokenize(self, expression: str) -> List[str]:
        if re.search(r'\d', expression):
            raise ValueError("Ошибка: выражение содержит числа или цифры, что недопустимо.")

        tokens = []
        for match in self.TOKEN_REGEX.finditer(expression):
            if match.group(1):
                tokens.append('(')
            elif match.group(2):
                tokens.append(')')
            elif match.group(3):
                tokens.append('|')
            elif match.group(4):
                tokens.append('*')
            elif match.group(5):
                tokens.append('!')
            elif match.group(6):
                tokens.append('+')
            elif match.group(7):
                tokens.append('>')
            elif match.group(8):
                tokens.append('=')
            elif match.group(9):
                tokens.append(match.group(9))
            else:
                raise ValueError(f"Недопустимый символ в выражении: '{expression[match.start()]}'")
        return tokens

    def parse(self) -> Expression:
        result = self.parse_equivalence()
        if self.pos < len(self.tokens):
            current = self.tokens[self.pos]
            raise ValueError(f"Некорректное выражение: неожиданный токен '{current}' на позиции {self.pos}")
        return result

    def current_token(self) -> Union[str, None]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume_token(self, expected: str = None) -> str:
        token = self.current_token()
        if token is None:
            raise ValueError(f"Ожидался токен , но достигнут конец выражения")
        if expected and token != expected:
            raise ValueError(f"Ожидался токен {expected}, но был {token}")
        self.pos += 1
        return token

    def parse_variable(self) -> Expression:
        token = self.current_token()
        if token is None:
            raise ValueError(f"Ожидалась переменная, но достигнут конец выражения на позиции {self.pos}")
        if re.fullmatch(r'[A-Za-z]', token):
            self.pos += 1
            return Variable(token)
        else:
            raise ValueError(f"Ожидалась переменная на позиции {self.pos}")

    def parse_parenthesized(self) -> Expression:
        token = self.current_token()
        if token == '(':
            self.consume_token('(')
            expr = self.parse_equivalence()
            self.consume_token(')')
            return expr
        else:
            return self.parse_variable()

    def parse_negation(self) -> Expression:
        token = self.current_token()
        if token == '!':
            self.consume_token('!')
            return Negation(self.parse_negation())
        else:
            return self.parse_parenthesized()

    def parse_conjunction(self) -> Expression:
        left = self.parse_negation()
        while self.current_token() == '*':
            self.consume_token('*')
            right = self.parse_negation()
            left = Negation(Implication(left, Negation(right)))
        return left

    def parse_disjunction(self) -> Expression:
        left = self.parse_conjunction()
        while self.current_token() == '|':
            self.consume_token('|')
            right = self.parse_conjunction()
            # Дизъюнкция выражена как (!A > B)
            left = Implication(Negation(left), right)
        return left

    def parse_xor(self) -> Expression:
        left = self.parse_disjunction()
        while self.current_token() == '+':
            self.consume_token('+')
            right = self.parse_disjunction()
            left = Implication(
                Implication(Negation(left), Negation(right)),
                Negation(Implication(left, right))
            )
        return left

    def parse_implication(self) -> Expression:
        left = self.parse_xor()
        while self.current_token() == '>':
            self.consume_token('>')
            right = self.parse_implication()
            left = Implication(left, right)
        return left

    def parse_equivalence(self) -> Expression:
        left = self.parse_implication()
        while self.current_token() == '=':
            self.consume_token('=')
            right = self.parse_implication()
            left = Implication(
                Implication(left, Negation(right)),
                Negation(Implication(Negation(left), right))
            )
        return left