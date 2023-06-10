#!/usr/bin/python3

# @file example script for tutorial 3: https://wp.me/p9qb6x-9f


from util import *
from algorithms import *

a1 = read("../pair_a_X_not_*bb*.dfa")
a2 = read("../*aaba*_neg.dfa")

p = product(a1, a2)
print(f"product of p and *aaba*_neg:\n {p}")

name = "pair_a_X_not_*bb*_X_*aaba*_neg"
save(p, f"../{name}.dfa")
to_png(p, f"../{name}.png", group=True)
