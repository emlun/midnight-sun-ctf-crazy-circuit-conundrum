#!/usr/bin/python3
#
# Script for generating a structurally simple but tangled Boolean function
# Copyright (C) 2018  Emil Lundberg <emil@emlun.se>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.


import random
import z3
from z3 import (
    And,
    Bool,
    Not,
    Or,
    Solver,
)


def Nor(a, b):
    return Not(Or(a, b))


def test_problem(problem):
    s = Solver()
    s.add(problem)
    return s.check() == z3.sat


def print_solution(problem):
    print(problem)
    print(z3.simplify(problem))

    s = Solver()
    s.add(problem)
    if s.check() == z3.sat:
        m = s.model()
        print(m)
    else:
        print('unsat')


def maybe_wrap_not(a, should_wrap):
    return Not(a) if should_wrap else a


def enlarge_problem(pin_queue, operator_queue, conditions):
    if len(pin_queue) == 0 or len(operator_queue) == 0:
        return conditions

    else:
        [lhs, rhs] = pin_queue[:2]
        operator = operator_queue[0]

        remaining_pins = pin_queue[2:]
        remaining_operators = operator_queue[1:]

        new_condition_candidates = [
            operator(
                maybe_wrap_not(lhs, not_lhs),
                maybe_wrap_not(rhs, not_rhs),
            )
            for (not_lhs, not_rhs) in zip(
                random.sample([True, False], k=2),
                random.sample([True, False], k=2),
            )
        ]

        valid_candidates = [
            candidate
            for candidate in new_condition_candidates if test_problem(And(*conditions, candidate))
        ]

        for cand in valid_candidates:
            solution = enlarge_problem(remaining_pins, remaining_operators, [*conditions, cand])
            if solution is not None:
                return solution


def build_problem():
    num_inputs = 16

    component_operators = [And, Nor]

    pins = [Bool('dip_%d' % i) for i in range(num_inputs)]

    operator_queue = random.sample(component_operators * (num_inputs // len(component_operators)), k=num_inputs)
    pin_queue = random.sample(pins * 2, k=num_inputs*2)

    return (pins, And(*enlarge_problem(pin_queue, operator_queue, [])))


def check_unique_solution(pins, problem):
    s = Solver()
    s.add(problem)

    print(problem)

    if s.check() == z3.sat:
        print(s.model())

        s.add(Not(model_to_condition(pins, s.model())))
        if s.check() == z3.sat:
            print(s.model())
            print('Solution not unique!')
        else:
            print('Solution is unique!')
    else:
        print('Not solvable!')


def model_to_condition(pins, model):
    return And(
        *[pin if bool(model[pin]) else Not(pin) for pin in pins]
    )


(pins, problem) = build_problem()
check_unique_solution(pins, problem)
