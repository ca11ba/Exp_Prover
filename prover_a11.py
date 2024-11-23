from expressions import *
from parser import Parser


class Proof:
    def __init__(self, formula: Expression):
        self.context = []  # Контекст гипотез
        self.target = formula  # Итоговая цель
        self.proven = False  # Флаг успешного доказательства
        self.steps = []  # Шаги доказательства

    def add_to_context(self, hypothesis: Expression):

        self.context.append(hypothesis)
        self.steps.append(f"Assume: {hypothesis.to_string()}")

    def check_goal(self) -> bool:
        for hypothesis in self.context:
            if hypothesis.to_string() == self.target.to_string():
                return True
        return False

    def decompose_implications(self):
        while isinstance(self.target, Implication):
            # Переносим левую часть импликации в гипотезы
            hypothesis = self.target.left
            self.add_to_context(hypothesis)

            # Если цель совпадает с гипотезой, доказательство завершено
            if self.check_goal():
                self.steps.append(f"Conclusion: {self.target.to_string()} (from context)")
                self.proven = True
                return

            # Обновляем цель
            self.target = self.target.right

    def prove(self):

        print("Proof steps:")

        # Разбираем импликации
        self.decompose_implications()

        # Проверяем вывод цели
        if not self.proven:
            if self.check_goal():
                self.steps.append(f"Conclusion: {self.target.to_string()} (from context)")
                self.proven = True
            else:
                self.steps.append(f"Unable to conclude: {self.target.to_string()} from context")

        # Вывод шагов доказательства
        for step in self.steps:
            print(step)

        # Итог
        if self.proven:
            print(f"Proven: {self.target.to_string()}")
        else:
            print(f"Failed to prove: {self.target.to_string()}")


# Универсальная функция для доказательства
def prove_any_formula(expression_str: str):

    print(f"Input: {expression_str}")

    # Парсинг формулы
    parser = Parser(expression_str)
    expression = parser.parse()

    # Создание объекта доказательства
    proof = Proof(expression)

    # Запуск доказательства
    proof.prove()


# Тестирование
if __name__ == "__main__":
    # Пример 1: Простая формула
    prove_any_formula("(A | B) > (A | B)")

    # Пример 2: Более сложная формула
    prove_any_formula("(A > B) > (B > C) > (A > B)")

    prove_any_formula("a | !a")






