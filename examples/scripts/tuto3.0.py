#!/usr/bin/python3

# @file example script for tutorial 3: https://wp.me/p9qb6x-9f


from util import *
from algorithms import *

a = read("../*aaba*.dfa")
a = negate(a)
print(f"negation of a:\n {a}")

save(a, "../*aaba*_neg.dfa")
to_png(a, "../*aaba*_neg.png", group=True)

print("negation of na.dfa:")
negate(read("../not_accessible.dfa")) # error