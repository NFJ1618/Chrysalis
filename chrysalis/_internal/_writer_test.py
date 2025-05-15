import pytest
from rich.console import Console
from chrysalis._internal._search import SearchStrategy
from chrysalis._internal._writer import TerminalUIWriter, Verbosity


def test_print_header_standard_output(capsys: pytest.CaptureFixture) -> None:
    writer = TerminalUIWriter(verbosity=Verbosity.ALL, pretty=False)
    writer.print_header(
        search_strategy=SearchStrategy.RANDOM,
        chain_length=10,
        num_chains=5,
    )
    captured = capsys.readouterr()
    assert "Search Strategy: RANDOM" in captured.out
    assert "Chain Length: 10" in captured.out
    assert "Num Chains: 5" in captured.out


def test_print_header_with_low_verbosity(capsys: pytest.CaptureFixture) -> None:
    writer = TerminalUIWriter(verbosity=Verbosity.SILENT, pretty=False)
    writer.print_header(
        search_strategy=SearchStrategy.RANDOM,
        chain_length=42,
        num_chains=3,
    )
    captured = capsys.readouterr()
    assert captured.out == ""


def test_print_header_pretty_mode() -> None:
    console = Console(record=True)
    writer = TerminalUIWriter(verbosity=Verbosity.ALL, pretty=True)
    writer._console = console

    writer.print_header(
        search_strategy=SearchStrategy.RANDOM,
        chain_length=20,
        num_chains=2,
    )

    output = console.export_text()
    assert "CHRYSALIS Metamorphic Test" in output
    assert "Search Strategy:" in output
    assert "RANDOM" in output
    assert "Chain Length:" in output
    assert "20" in output
    assert "Num Chains:" in output
    assert "2" in output


def test_print_tested_relation_standard(capsys: pytest.CaptureFixture) -> None:
    writer = TerminalUIWriter(verbosity=Verbosity.FAILURE, pretty=False)

    writer.print_tested_relation(success=True)
    writer.print_tested_relation(success=False)

    captured = capsys.readouterr()
    assert "." in captured.out
    assert "F" in captured.out


def test_print_tested_relation_pretty() -> None:
    console = Console(record=True)
    writer = TerminalUIWriter(verbosity=Verbosity.ALL, pretty=True)
    writer._console = console
    writer.start_live()

    writer.print_tested_relation(success=True, metadata={"relation": "foo", "index": 1})
    writer.print_tested_relation(
        success=False,
        metadata={"relation": "bar", "index": 2, "failed_invariants": ["inv1"]},
    )

    writer.stop_live()

    output = console.export_text()
    assert "." in output or "✔" in output or "F" in output or "✘" in output
    assert "relation" in output
    assert "foo" in output
    assert "bar" in output
    assert "inv1" in output


def test_print_failed_relations_standard(capsys: pytest.CaptureFixture) -> None:
    writer = TerminalUIWriter(verbosity=Verbosity.FAILURE, pretty=False)

    writer.store_failed_relation(
        failed_relation="rel_identity_preserves_shape",
        failed_invariants=["shape_unchanged", "not_null"],
    )
    writer.print_failed_relations()
    captured = capsys.readouterr()

    assert "rel_identity_preserves_shape" in captured.out
    assert "shape_unchanged" in captured.out
    assert "not_null" in captured.out


def test_print_failed_relations_pretty() -> None:
    console = Console(record=True)
    writer = TerminalUIWriter(verbosity=Verbosity.FAILURE, pretty=True)
    writer._console = console

    writer.store_failed_relation(
        failed_relation="rel_sort_stability", failed_invariants=["order_preserved"]
    )
    writer.print_failed_relations()
    output = console.export_text()

    assert "rel_sort_stability" in output
    assert "order_preserved" in output


def test_print_summary_standard(capsys: pytest.CaptureFixture) -> None:
    writer = TerminalUIWriter(verbosity=Verbosity.ALL, pretty=False)

    writer._success_count = 3
    writer._failure_count = 1
    writer.print_summary()
    captured = capsys.readouterr()

    assert "Passed: 3" in captured.out
    assert "Failed: 1" in captured.out


def test_print_summary_pretty() -> None:
    console = Console(record=True)
    writer = TerminalUIWriter(verbosity=Verbosity.ALL, pretty=True)
    writer._console = console

    writer._success_count = 2
    writer._failure_count = 2
    writer.print_summary()
    output = console.export_text()

    assert "✔ Passed" in output
    assert "✘ Failed" in output
