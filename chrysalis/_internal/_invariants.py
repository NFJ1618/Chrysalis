"""
A collection of simple but useful invariants.

In an attempt to reduce boiler plate code, we provide an ever-growing collection of
simple invariants. This module is designed to be imported in its totality so that each
invariant can be used by simply specifying an attribute of the module. This removes the
need of the user to define their own functions for these simple invaraints (especially
since we don't allow users to use lambda functions for invariants).

This collection can be added to as collaborators see fit. General guidelines for adding
a new invariant are as follows:
- The new invariant is general
- The new invariant is easy to understand at a moment's glance
"""


def equals[T](curr: T, prev: T) -> bool:
    return curr == prev


def not_equals[T](curr: T, prev: T) -> bool:
    return curr != prev


def is_same_sign(curr: float, prev: float) -> bool:
    return curr >= 0 and prev >= 0 or curr <= 0 and prev <= 0


def not_same_sign(curr: float, prev: float) -> bool:
    return not is_same_sign(curr, prev)


def greater_than(curr: float, prev: float) -> bool:
    return curr > prev


def greater_than_equal(curr: float, prev: float) -> bool:
    return curr >= prev


def less_than(curr: float, prev: float) -> bool:
    return curr < prev


def less_than_equal(curr: float, prev: float) -> bool:
    return curr <= prev
