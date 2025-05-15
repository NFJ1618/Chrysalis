from __future__ import annotations

import shutil
from collections.abc import Callable
from enum import IntEnum
from functools import cache
from typing import NamedTuple

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn
from rich.live import Live

from chrysalis._internal._search import SearchStrategy

# ASCII ART Credit: https://patorjk.com/software/taag.
_ASCII_ART_CHRYSALIS = """
   _____ _                          _ _
  / ____| |                        | (_)
 | |    | |__  _ __ _   _  __ _ ___| |_ ___
 | |    | '_ \\| '__| | | |/ _` / __| | / __|
 | |____| | | | |  | |_| | (_| \\__ | | \\__ \\
  \\_____|_| |_|_|   \\__, |\\__,_|___|_|_|___/
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
        pretty: bool = False,
        total_relations: int | None = None
    ) -> None:
        self._verbosity = verbosity
        self._pretty = pretty
        self._console = Console() if pretty else None
        self._failed_relations: list[FailedInvaraint[T, R]] = []
        
        self._live_display = None
        self._result_bar = Text()
        
        self._success_count = 0
        self._failure_count = 0

        self._progress = None
        self._progress_task = None

        if pretty and total_relations:
            self._progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                "[green]{task.completed}/{task.total}[/]",
                TimeElapsedColumn(),
                console=self._console,
                transient=True,
            )
            self._progress_task = self._progress.add_task(
                "[cyan]Testing Relations...", total=total_relations
            )

    @min_verbosity_level(verbosity=Verbosity.FAILURE)
    def print_header(
        self,
        search_strategy: SearchStrategy,
        chain_length: int,
        num_chains: int,
    ) -> None:
        if self._pretty:
            self._console.print(Panel(Text("CHRYSALIS Metamorphic Test", justify="center", style="bold magenta")))
            self._console.print(f"[bold cyan]Search Strategy:[/] {search_strategy.name}")
            self._console.print(f"[bold cyan]Chain Length:[/] {chain_length}")
            self._console.print(f"[bold cyan]Num Chains:[/] {num_chains}")
            self._console.print()            
        else:
            print(_ASCII_ART_CHRYSALIS)
            print(f"Search Strategy: {search_strategy.name}")
            print(f"Chain Length: {chain_length}")
            print(f"Num Chains: {num_chains}")
            print()

    def _print_tested_relation_level_failure(self, success: bool) -> None:
        if self._pretty and self._progress:
            self._progress.update(self._progress_task, advance=1)
        else:
            print("." if success else "F", end="")
        if success:
            self._success_count += 1
        else:
            self._failure_count += 1

    
    def start_live(self):
        if self._pretty and self._verbosity == Verbosity.ALL:
            self._live_display = Live(self._result_bar, console=self._console, refresh_per_second=10)
            self._live_display.start()

    def stop_live(self):
        if self._live_display:
            self._live_display.stop()
            self._live_display = None
    
    def _print_tested_relation_level_all(self, success: bool, metadata: dict | None = None) -> None:
        char = "[green].[/]" if success else "[red]F[/]"
        self._result_bar.append(char)
        if self._live_display:
            self._live_display.update(self._result_bar)

        if not success:
            self._console.print("\n[bold red]Failure[/bold red]")
            if metadata:
                for key, value in metadata.items():
                    self._console.print(f"[red]- {key}:[/] {value}")
        elif metadata and self._verbosity == Verbosity.ALL:
            self._console.print(f"[green]✔ Success:[/] {metadata}")


    @min_verbosity_level(verbosity=Verbosity.FAILURE)
    def print_tested_relation(self, success: bool, *, metadata: dict | None = None) -> None:
        if self._verbosity == Verbosity.FAILURE:
            self._print_tested_relation_level_failure(success=success)
        else:
            self._print_tested_relation_level_all(success=success, metadata=metadata)

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
        if self._pretty:
            table = Table(title="Failed Relations", show_lines=True)
            table.add_column("Relation", style="red bold")
            table.add_column("Failed Invariants", style="yellow")

            for fr in self._failed_relations:
                table.add_row(fr.failed_relation, "\n".join(fr.failed_invariants))

            self._console.print()
            self._console.print(table)
        else:
            print()
            print("=" * get_terminal_size())
            print()
            for failed_relation in self._failed_relations:
                print(f"Failed Relation: {failed_relation.failed_relation}")
                print(f"Failed Invariants: {failed_relation.failed_invariants}")
                print("=" * get_terminal_size())
                print()

    def print_summary(self, time_taken: float) -> None:
        if self._pretty:
            self._console.print()
            self._console.rule("[bold green]Summary")
            self._console.print(f"[green]✔ Passed:[/] {self._success_count}")
            self._console.print(f"[red]✘ Failed:[/] {self._failure_count}")
            self._console.print(f"[blue]🕒 Time:[/] {time_taken:.2f}s")
        else:
            print()
            print("Summary")
            print(f"Passed: {self._success_count}")
            print(f"Failed: {self._failure_count}")
            print(f"Time: {time_taken:.2f}s")

    def start_progress(self) -> None:
        if self._pretty and self._progress:
            self._progress.start()

    def stop_progress(self) -> None:
        if self._pretty and self._progress:
            self._progress.stop()