#!/usr/bin/python3

# @file example script for tutorial: https://wp.me/p9qb6x-9f

import util
from algorithms import *
a = util.read("../*aaba*.dfa")

successors(a, a.init)
['1', '0']

for state in a.states:
    print("successors(" + state + ")   = " + str(successors(a, state)))
    print("predecessors(" + state + ") = " + str(predecessors(a, state)))
