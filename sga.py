import argparse
import string
import itertools
import operator
import random

PRIME_CONSTANTS = {
    1: [3, 5, 7],
    2: [11, 13, 17],
    3: [19, 23, 29],
    4: [31, 37, 41],
    5: [43, 47, 53],
    6: [59, 61, 67],
    7: [71, 73, 79],
    8: [83, 89, 97],
    9: [101, 103, 107],
}

GEOMETRIC_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}

class Node:
    def __init__(self, left, right, op, indexes):
        self.left = left
        self.right = right
        self.op = op
        self.indexes = indexes
    
    def calculate(self):
        try:
            left = self.left.calculate() if isinstance(self.left, Node) else self.left
            right = self.right.calculate() if isinstance(self.right, Node) else self.right
            if left is None or right is None:
                return None
            return GEOMETRIC_OPS[self.op](left, right)
        except ZeroDivisionError:
            return None
    
    def render(self):
        left = self.left.render() if isinstance(self.left, Node) else str(self.left)
        right = self.right.render() if isinstance(self.right, Node) else str(self.right)
        return f'({left} {self.op} {right})'

    @staticmethod
    def generate(roll_permutation, operation_permutation, operation_order):
        branches = list(roll_permutation)
        for op_index in operation_order:
            left = branches[op_index]
            right = branches[op_index + 1]
            indexes = []
            if isinstance(left, Node):
                indexes += left.indexes
            else:
                indexes.append(op_index)
            if isinstance(right, Node):
                indexes += right.indexes
            else:
                indexes.append(op_index + 1)
            node = Node(branches[op_index], branches[op_index + 1], operation_permutation[op_index], indexes)
            for i in indexes:
                branches[i] = node
        return branches[0]

def find_prime_combination(rolls, target):
    num_ops = len(rolls) - 1
    possible_ops = [op for op in GEOMETRIC_OPS.keys() for _ in range(num_ops)]
    for roll_permutation in itertools.permutations(rolls):
        for operation_permutation in itertools.permutations(possible_ops, num_ops):
            for operation_order in itertools.permutations(range(len(rolls) - 1)):
                tree = Node.generate(roll_permutation, operation_permutation, operation_order)
                if tree.calculate() in target:
                    return tree
    return None

def prime_helper_1(rolls, targets):
    if len(rolls) == 0:
        return None
    elif len(rolls) == 1:
        for op in GEOMETRIC_OPS:
            if GEOMETRIC_OPS[op](rolls[0], rolls[1]) in targets:
                return [rolls[0], op, rolls[1]]
        return None
    else:
        for subset_length in range(1, len(rolls)):
            for subset in itertools.combinations(rolls, subset_length):
                prime_helper_1(subset, targets)


def find_prime_combination_2(rolls, targets):
    return prime_helper_1(set(rolls), set(targets))

def sacred_geometry():
    pass

LETTER_VALUES = {
    1: "ajs",
    2: "bkt",
    3: "clu",
    4: "dmv",
    5: "enw",
    6: "fox",
    7: "gpy",
    8: "hqz",
    9: "ir",
}
def calc_letter_val(letter):
    for value in LETTER_VALUES:
        if letter in LETTER_VALUES[value]:
            return value
    return None

LETTER_MAP = {
    letter: calc_letter_val(letter) for letter in string.ascii_lowercase
}

def arithmancy(spell_name):
    total = sum([LETTER_MAP[letter] for letter in spell_name.lower()])
    while total // 10 > 0:
        total = sum([int(letter) for letter in str(total)])
    return total

def main():
    print(f'arithmancy(Fireball) = {arithmancy("Fireball")}')
    rolls = [random.randint(1, 6) for _ in range(20)]
    print(rolls)
    tree = find_prime_combination(rolls, PRIME_CONSTANTS[9])
    print(f'sacred_geometry(magic missile) = {tree.render()} = {tree.calculate()}')

if __name__ == "__main__":
    main()