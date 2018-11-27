import sys

sys.path.insert(0, '../src')

import algorithms as alg
from DFA import *

a = DFA("abc")

a.add_state("0")
a.add_state("1")
a.add_state("2")
a.add_state("3", True)
a.init = "0"

a.add_transition("0", "a", "1")
a.add_transition("0", "b", "0")
a.add_transition("1", "a", "2")
a.add_transition("1", "b", "0")
a.add_transition("2", "a", "2")
a.add_transition("2", "b", "3")
a.add_transition("3", "a", "3")
a.add_transition("3", "b", "3")

print(a)

strs = ["aabaa", "babaab", "abababaabaa", "bababbaabaaabaabababaabab", "babaaabbab", "aabac", "bababb"]

for str in strs:
    if alg.run(a, str, True):
        print("Word '" + str + "' accepted.")
    else:
        print("Word '" + str + "' rejected.")
