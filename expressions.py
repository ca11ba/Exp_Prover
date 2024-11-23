# expressions.py
class Expression:
    def to_string(self) -> str:
        raise NotImplementedError("Метод должен быть переопределен в подклассах.")

class Variable(Expression):
    def __init__(self, name: str):
        self.name = name

    def to_string(self) -> str:
        return self.name

class Negation(Expression):
    def __init__(self, operand: Expression):
        self.operand = operand

    def to_string(self) -> str:
        return f"!{self.operand.to_string()}"

class Conjunction(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def to_string(self) -> str:
        return f"({self.left.to_string()} * {self.right.to_string()})"

class Disjunction(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def to_string(self) -> str:
        return f"({self.left.to_string()} | {self.right.to_string()})"

class ExclusiveOr(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def to_string(self) -> str:
        return f"({self.left.to_string()} + {self.right.to_string()})"

class Implication(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def to_string(self) -> str:
        return f"({self.left.to_string()} > {self.right.to_string()})"

class Equivalence(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def to_string(self) -> str:
        return f"({self.left.to_string()} = {self.right.to_string()})"