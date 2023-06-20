#!/usr/bin/python3

# @file example script for tutorial 4: https://wp.me/p9qb6x-ae


from util import *
from algorithms import *

a = read("../minimization2.dfa")
name = "minimization2"
save(a, f"../{name}.dfa")
to_png(a, f"../{name}.png", group=True)

print("a = {a}")

m = minimize(a)

print(f"minimized = {m}")


name = "minimized2"
save(m, f"../{name}.dfa")
to_png(m, f"../{name}.png", group=True)