#!/usr/bin/python3

# @file example script for tutorial 1: https://wp.me/p9qb6x-7n

import DFA

# Create DFA
a = DFA.DFA("ab")
a.add_state("0")
a.add_state("1", True)
a.init = "0"
a.add_transition("0", "a", "1")
a.add_transition("0", "b", "0")
a.add_transition("1", "a", "1")
a.add_transition("1", "b", "1")
print(a)

