#!/usr/bin/python3

# @file example script for tutorial 2: https://wp.me/p9qb6x-9f

import util
from algorithms import *

aaba = util.read("../*aaba*.dfa")
print(f"aaba is complete: {is_complete(aaba)}")

abc = util.read("../abc*.dfa")
print(f"abc is complete: {is_complete(abc)}")

a = complete(abc.clone())
print(f"Complete(a): {a}")

print(f"Is complete: {is_complete(a)}")

util.save(a, "../abc*_complete.dfa")
util.to_png(a, "../abc*_complete.png", group=True)
 