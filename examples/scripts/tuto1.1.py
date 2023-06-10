#!/usr/bin/python3

# @file example script for tutorial: https://wp.me/p9qb6x-7n

import DFA
a = DFA.DFA("ab")

a.add_state("0")
a.add_state("1")
a.add_state("2")
a.add_state("3")
a.add_state("4", True)
a.init = "0"

a.add_transition("0", "a", "1")
a.add_transition("0", "b", "0")
a.add_transition("1", "a", "2")
a.add_transition("1", "b", "0")
a.add_transition("2", "a", "2")
a.add_transition("2", "b", "3")
a.add_transition("3", "a", "4")
a.add_transition("3", "b", "0")
a.add_transition("4", "a", "4")
a.add_transition("4", "b", "4")

print(a)

from algorithms import run

tests = ["aabaabaa", "bbababaabba"]
for s in tests:
    print(f"Running DFA with {s}")
    run(a, s, True)

import util
util.save(a, "tuto1.1_*aaba*.dfa")
