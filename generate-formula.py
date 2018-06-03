#!/usr/bin/python3

import random


def count_operator(components, operator):
    return sum([(1 if c[1] == operator else 0) for c in components])


def format_component(component):
    (lhs, op, rhs, not_lhs, not_rhs) = component
    return '%s %s %s' % (
        'not(%s)' % lhs if component[3] else lhs,
        op,
        'not(%s)' % rhs if component[4] else rhs,
    )


num_inputs = 16

# component_operators = ['and', 'or', 'xor', 'nor', 'nand']
component_operators = ['and', 'nor']
overall_operator = 'and'

inputs = ['i' + str(i) for i in range(1, num_inputs + 1)]

operators_to_choose_from = random.sample(component_operators, num_inputs // 4) if len(component_operators) > 4 else component_operators
operators_to_choose_from = operators_to_choose_from * (num_inputs // len(component_operators))
operators_to_choose_from.sort()

components = [(lhs, op, rhs, not_lhs, not_rhs) for (lhs, op, rhs, not_lhs, not_rhs) in zip(random.sample(inputs, num_inputs), operators_to_choose_from, random.sample(inputs, num_inputs), random.choices([True, False], k=num_inputs), random.choices([True, False], k=num_inputs))]


print('and( (' + '), ('.join([format_component(c) for c in components]) + ') )')

for op in component_operators:
    print('%s: %d' % (op, count_operator(components, op)))

print('not: %d' % sum([(1 if c[3] else 0) + (1 if c[4] else 0) for c in components]))
print('self: %d' % sum([1 if c[0] == c[2] else 0 for c in components]))
