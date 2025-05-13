from __future__ import annotations

import shutil
from collections.abc import Callable
from enum import IntEnum
from functools import cache
from typing import NamedTuple

from chrysalis._internal._search import SearchStrategy

# ASCII ART Credit: https://patorjk.com/software/taag.
_ASCII_ART_CHRYSALIS = """
   _____ _                          _ _     
  / ____| |                        | (_)    
 | |    | |__  _ __ _   _ ___  __ _| |_ ___ 
 | |    | '_ \\| '__| | | / __|/ _` | | / __|
 | |____| | | | |  | |_| \\__ \\ (_| | | \\__ \\
  \\_____|_| |_|_|   \\__, |___/\\__,_|_|_|___/
                     __/ |                  
                    |___/                   
"""


class Verbosity(IntEnum):
    SILENT = 1
    FAILURE = 2
    ALL = 3


def min_verbosity_level(verbosity: Verbosity):
    def check_verbosity(
        func: Callable[..., None],
    ) -> Callable[..., None]:
        def wrapper(self: TerminalUIWriter, *args, **kwargs) -> None:
            if self._verbosity >= verbosity:
                func(self, *args, **kwargs)

        return wrapper

    return check_verbosity


class FailedInvaraint[T, R](NamedTuple):
    failed_relation: str
    # pre_transform_data: T
    # post_transform_data: T
    # pre_transform_result: R
    # post_transform_result: R
    failed_invariants: list[str]


@cache
def get_terminal_size() -> int:
    return shutil.get_terminal_size().columns


class TerminalUIWriter[T, R]:
    def __init__(
        self,
        verbosity: Verbosity = Verbosity.FAILURE,
    ) -> None:
        self._verbosity = verbosity
        self._failed_relations: list[FailedInvaraint[T, R]] = []

    @min_verbosity_level(verbosity=Verbosity.FAILURE)
    def print_header(
        self,
        search_strategy: SearchStrategy,
        chain_length: int,
        num_chains: int,
    ) -> None:
        print("\033[35m" + _ASCII_ART_CHRYSALIS + "\033[0m")
        print(f"Search Strategy: {search_strategy.name}")
        print(f"Chain Length: {chain_length}")
        print(f"Num Chains: {num_chains}")
        print()

    def _print_tested_relation_level_failure(self, success: bool) -> None:
        if success:
            print(".", end="", flush=True)
        else:
            print("F", end="", flush=True)

    def _print_tested_relation_level_all(self, success: bool) -> None:
        raise NotImplementedError

    @min_verbosity_level(verbosity=Verbosity.FAILURE)
    def print_tested_relation(self, success: bool) -> None:
        if self._verbosity == Verbosity.FAILURE:
            self._print_tested_relation_level_failure(success=success)
        else:
            self._print_tested_relation_level_all(success=success)

    @min_verbosity_level(verbosity=Verbosity.FAILURE)
    def store_failed_relation(
        self,
        # pre_transform_data: T,
        # post_transform_data: T,
        # pre_transform_result: R,
        # post_transform_result: R,
        failed_relation: str,
        failed_invariants: list[str],
    ) -> None:
        self._failed_relations.append(
            FailedInvaraint(
                failed_relation=failed_relation,
                # pre_transform_data=pre_transform_data,
                # post_transform_data=post_transform_data,
                # pre_transform_result=pre_transform_result,
                # post_transform_result=post_transform_result,
                failed_invariants=failed_invariants,
            )
        )

    @min_verbosity_level(verbosity=Verbosity.FAILURE)
    def print_failed_relations(self) -> None:
        print()
        print("=" * get_terminal_size())
        print()

        for failed_relation in self._failed_relations:
            print(f"Failed Relation: {failed_relation.failed_relation}")
            # print(f"Pre-Transformed Data: {failed_relation.pre_transform_data}")
            # print(f"Post-Transformed Data: {failed_relation.post_transform_data}")
            # print(f"Pre-Transformed Result: {failed_relation.pre_transform_result}")
            # print(f"Post-Transformed Result: {failed_relation.post_transform_result}")
            print(f"Failed Invariants: {failed_relation.failed_invariants}")

            print("=" * get_terminal_size())
            print()
