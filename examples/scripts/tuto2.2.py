#!/usr/bin/python3

# @file example script for tutorial 2: https://wp.me/p9qb6x-9f

import util
from algorithms import *

a = util.read("../not_accessible.dfa")
print(f"a is accessible: {accessible(a)}")
print(f"a is coaccessible: {coaccessible(a)}")

a2 = util.read("../abc*_complete.dfa")
print(f"abc* is accessible: {accessible(a2)}")
print(f"abc* is coaccessible: {coaccessible(a2)}")


print(f"accessible states for a: {accessible_states(a)}")
print(f"accessible states for abc*: {accessible_states(a2)}")
print(f"coaccessible states for a: {coaccessible_states(a)}")
print(f"coaccessible states for abc*: {coaccessible_states(a2)}")