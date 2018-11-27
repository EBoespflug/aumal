import sys

sys.path.insert(0, '../src')

import algorithms as alg
from DFA import *

a = DFA("012")

a.add_state("0", True)
a.add_state("1")
a.add_state("2")
a.add_state("3")
a.init = "0"

a.add_transition("0", "0", "0")
a.add_transition("0", "1", "1")
a.add_transition("0", "2", "2")
a.add_transition("1", "0", "3")
a.add_transition("1", "1", "0")
a.add_transition("1", "2", "2")
a.add_transition("2", "0", "2")
a.add_transition("2", "1", "3")
a.add_transition("2", "2", "0")
a.add_transition("3", "0", "1")
a.add_transition("3", "1", "2")
a.add_transition("3", "2", "3")

print(a)

strs = ["0", "1", "2", "10", "11", "12", "20", "21", "22", "100", "101", "102", "110", "111", "112", "120", "121", "122",
    "200", "201", "202", "210", "211", "220", "221", "222", "1000", "1001"]

for str in strs:
    if alg.run(a, str):
        print("Word '" + str + "' accepted.")
    else:
        print("Word '" + str + "' rejected.")
