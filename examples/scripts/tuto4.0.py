#!/usr/bin/python3

# @file example script for tutorial 4: https://wp.me/p9qb6x-ae


from util import *
from algorithms import *

a1 = read("../minimisation.dfa")
#a2 = read("../*aaba*_neg.dfa")

print("a = {a1}")

m = minimize(a1)

print(f"minimized = {m}")


name = "minimized"
save(m, f"../{name}.dfa")
to_png(m, f"../{name}.png", group=True)