#!/usr/bin/python3

# @file example script for tutorial 3: https://wp.me/p9qb6x-9f


from util import *
from algorithms import *

pair_a = read("../pair_a.dfa")
not_bb = read("../not_*bb*.dfa")

p = product(pair_a, not_bb)
print(f"product of pair_a and not_bb:\n {p}")

name = "pair_a_X_not_*bb*"
save(p, f"../{name}.dfa")
to_png(p, f"../{name}.png", group=True)
