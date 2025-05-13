import pytest

from chrysalis._internal._search import SearchStrategy
from chrysalis._internal._writer import TerminalUIWriter, Verbosity


def test_print_header(capsys: pytest.CaptureFixture) -> None:
    writer = TerminalUIWriter(verbosity=Verbosity.ALL)
    writer.print_header(
        search_strategy=SearchStrategy.RANDOM,
        chain_length=10,
        num_chains=5,
    )
