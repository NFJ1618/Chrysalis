import polars as pl


def length_equals(curr: pl.DataFrame, prev: pl.DataFrame) -> bool:
    return len(curr) == len(prev)


def length_greater_than_equals(curr: pl.DataFrame, prev: pl.DataFrame) -> bool:
    return len(curr) >= len(prev)


def length_less_than_equals(curr: pl.DataFrame, prev: pl.DataFrame) -> bool:
    return len(curr) <= len(prev)
