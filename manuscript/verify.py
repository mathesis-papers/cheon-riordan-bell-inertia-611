import itertools
import json
from fractions import Fraction


def multiply_polynomials(left, right, length):
    product = [0] * length
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            degree = left_degree + right_degree
            if degree < length:
                product[degree] += left_value * right_value
    return product


def bell_adjacency(order, coefficients):
    length = max(1, order - 1)
    series = (list(coefficients) + [0] * length)[:length]
    bell_parameter = ([0] + series)[:length]
    power = [1] + [0] * (length - 1)
    matrix = [[0] * order for row in range(order)]
    for column in range(order):
        column_series = multiply_polynomials(series, power, length)
        for row in range(column + 1, order):
            matrix[row][column] = column_series[row - 1] % 2
            matrix[column][row] = matrix[row][column]
        power = multiply_polynomials(power, bell_parameter, length)
    return matrix


def matrix_product(left, right):
    return [[sum(left[row][inner] * right[inner][column]
                 for inner in range(len(right)))
             for column in range(len(right[0]))] for row in range(len(left))]


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def determinant(matrix):
    reduced = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    for column in range(len(matrix)):
        pivot = next((row for row in range(column, len(matrix))
                      if reduced[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            reduced[pivot], reduced[column] = reduced[column], reduced[pivot]
            answer = -answer
        diagonal = reduced[column][column]
        answer *= diagonal
        for row in range(column + 1, len(matrix)):
            factor = reduced[row][column] / diagonal
            for entry in range(column + 1, len(matrix)):
                reduced[row][entry] -= factor * reduced[column][entry]
    return answer


def inertia(matrix):
    reduced = [[Fraction(value) for value in row] for row in matrix]
    positive = negative = 0
    while reduced:
        size = len(reduced)
        pivot = next((index for index in range(size) if reduced[index][index]), None)
        if pivot is not None:
            remaining = [index for index in range(size) if index != pivot]
            diagonal = reduced[pivot][pivot]
            positive += diagonal > 0
            negative += diagonal < 0
            reduced = [[reduced[row][column]
                        - reduced[row][pivot] * reduced[pivot][column] / diagonal
                        for column in remaining] for row in remaining]
            continue
        pair = next(((row, column) for row in range(size)
                     for column in range(row + 1, size) if reduced[row][column]), None)
        if pair is None:
            return positive, negative, size
        left, right = pair
        remaining = [index for index in range(size) if index not in pair]
        off_diagonal = reduced[left][right]
        reduced = [[reduced[row][column]
                    - (reduced[row][left] * reduced[right][column]
                       + reduced[row][right] * reduced[left][column]) / off_diagonal
                    for column in remaining] for row in remaining]
        positive += 1
        negative += 1
    return positive, negative, 0


def cycle_adjacency(order):
    return [[int((row - column) % order in (1, order - 1))
             for column in range(order)] for row in range(order)]


def cycle_inertia(order):
    quotient, residue = divmod(order, 4)
    return [(2 * quotient - 1, 2 * quotient - 1, 2),
            (2 * quotient + 1, 2 * quotient, 0),
            (2 * quotient + 1, 2 * quotient + 1, 0),
            (2 * quotient + 1, 2 * quotient + 2, 0)][residue]


def is_bipartite(matrix):
    colors = {}
    for vertex in range(len(matrix)):
        if vertex in colors:
            continue
        colors[vertex] = 0
        pending = [vertex]
        while pending:
            current = pending.pop()
            for neighbor, adjacent in enumerate(matrix[current]):
                if not adjacent:
                    continue
                if neighbor in colors:
                    if colors[neighbor] == colors[current]:
                        return False
                else:
                    colors[neighbor] = 1 - colors[current]
                    pending.append(neighbor)
    return True


def main():
    witness = bell_adjacency(5, [1, 0, 0, 1])
    assert witness == cycle_adjacency(5)
    change = [[1, 1, -1, -1, 1], [1, -1, 0, 0, -1],
              [0, 0, 1, 1, -1], [0, 0, 1, -1, 1], [0, 0, 0, 0, 1]]
    diagonal_values = [2, -2, 2, -2, 2]
    diagonal = [[diagonal_values[row] if row == column else 0
                 for column in range(5)] for row in range(5)]
    assert determinant(change) == 4
    assert determinant(witness) == 2
    assert matrix_product(matrix_product(transpose(change), witness), change) == diagonal
    assert inertia(witness) == (3, 2, 0)
    assert inertia([[0]]) == (0, 0, 1)
    assert inertia([[0, 1], [1, 0]]) == (1, 1, 0)
    assert inertia([[1, 0], [0, -1]]) == (1, 1, 0)
    cycles = []
    for order in range(3, 50):
        coefficients = [1] + [0] * (order - 3) + [1]
        matrix = bell_adjacency(order, coefficients)
        assert matrix == cycle_adjacency(order)
        computed = inertia(matrix)
        assert computed == cycle_inertia(order)
        cycles.append({'order': order, 'inertia': computed})
    prefixes = []
    proper_prefixes = 0
    for order in range(1, 9):
        count = 0
        counterexamples = 0
        even_series = 0
        for coefficients in itertools.product([0, 1], repeat=max(0, order - 1)):
            matrix = bell_adjacency(order, coefficients)
            computed = inertia(matrix)
            assert sum(computed) == order
            assert max(computed[:2]) <= (order + 1) // 2
            assert all(matrix[row][column] == 0
                       for row in range(1, order, 2)
                       for column in range(1, order, 2))
            if order % 2 == 0 and computed[2] == 0:
                assert computed[0] == computed[1] == order // 2
            count += 1
            counterexamples += computed[0] > computed[1]
            if all(value == 0 for degree, value in enumerate(coefficients) if degree % 2):
                assert computed[0] == computed[1]
                even_series += 1
            if order == 1 or coefficients[0] == 1:
                proper_prefixes += 1
                condition = all(value == 0 for degree, value in enumerate(coefficients)
                                if degree % 2)
                assert is_bipartite(matrix) == condition
            if order >= 3:
                target = (1,) + (0,) * (order - 3) + (1,)
                assert (matrix == cycle_adjacency(order)) == (coefficients == target)
        prefixes.append({'order': order, 'binary_prefixes': count,
                         'positive_exceeds_negative': counterexamples,
                         'even_series_equal_inertia': even_series})
    minimality = []
    for order in range(1, 5):
        edges = list(itertools.combinations(range(order), 2))
        count = 0
        for choices in itertools.product([0, 1], repeat=len(edges)):
            matrix = [[0] * order for row in range(order)]
            for (left, right), value in zip(edges, choices):
                matrix[left][right] = matrix[right][left] = value
            computed = inertia(matrix)
            assert computed[0] <= computed[1]
            count += 1
        minimality.append({'order': order, 'labelled_simple_graphs': count})
    sharpness = []
    for order in range(2, 50):
        matrix = bell_adjacency(order, [1]) if order % 2 == 0 else cycle_adjacency(order)
        computed = inertia(matrix)
        assert max(computed[:2]) == (order + 1) // 2
        sharpness.append({'order': order, 'inertia': computed})
    converse = bell_adjacency(4, [1, 1, 0])
    assert converse == [[0, 1, 1, 0], [1, 0, 1, 0],
                        [1, 1, 0, 1], [0, 0, 1, 0]]
    assert determinant(converse) == 1
    assert inertia(converse) == (2, 2, 0)
    assert not is_bipartite(converse)
    print(json.dumps({'arithmetic': 'integers and exact rational Schur complements',
                      'witness': {'order': 5, 'coefficients': [1, 0, 0, 1],
                                  'adjacency': witness, 'change_of_basis': change,
                                  'change_determinant': 4, 'adjacency_determinant': 2,
                                  'congruence_diagonal': diagonal_values, 'inertia': [3, 2, 0]},
                      'cycle_family': cycles, 'all_binary_prefixes': prefixes,
                      'proper_prefix_bipartiteness_cases': proper_prefixes,
                      'all_simple_graphs_minimality': minimality,
                      'absolute_bound_sharpness': sharpness,
                      'equal_inertia_nonbipartite': {'adjacency': converse,
                                                   'determinant': 1,
                                                   'inertia': [2, 2, 0]}},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
