import ast
import pickle
from pathlib import Path

from chrysalis._internal._engine import Engine, TemporarySqlite3RelationConnection
from chrysalis._internal._relation import Relation
from chrysalis._internal.conftest import eval_expr


def test_temporary_sqlite_db_deletes() -> None:
    with TemporarySqlite3RelationConnection() as (_, db_path):
        pass
    assert not db_path.exists()


def test_temporary_sqlite_db_deletes_error() -> None:
    p: Path | None = None
    try:
        with TemporarySqlite3RelationConnection() as (_, db_path):
            p = db_path
            raise RuntimeError(  # NOQA: TRY301
                "This runtime error is designed to ensure the sqlite database is deleted even if an error occurs during execution."
            )
    except Exception:  # NOQA: BLE001
        assert p is not None
        assert not p.exists()


def test_successful_relation_chain(
    sample_expression_1: ast.Expression,
    correct_relation_chain: list[Relation[ast.Expression, float]],
) -> None:
    with TemporarySqlite3RelationConnection() as (temp_conn, db_path):
        engine = Engine(
            sut=eval_expr,
            sqlite_conn=temp_conn,
            input_data=[sample_expression_1],
            sqlite_db=db_path,
            num_processes=1,
        )
        engine.execute([correct_relation_chain])
        conn = engine.results_to_duckdb()

    match conn.execute("SELECT * FROM input_data;").fetchall():
        case ((_, obj),):
            assert ast.unparse(pickle.loads(obj)) == ast.unparse(sample_expression_1)
        case _:
            raise ValueError(
                "Error extracting sample expression from returned duckdb connection."
            )

    assert [
        ("identity", 0),
        ("inverse", 1),
        ("subtract_1_from_expression", 2),
    ] == conn.execute(
        """
SELECT name, link_index
FROM applied_transformation
ORDER BY link_index;
                 """
    ).fetchall()

    assert conn.execute("SELECT COUNT(*) FROM failed_invariant").fetchall() == [(0,)]


def test_unsuccessful_relation_chain(
    sample_expression_1: ast.Expression,
    incorrect_relation_chain: list[Relation[ast.Expression, float]],
) -> None:
    with TemporarySqlite3RelationConnection() as (temp_conn, db_path):
        engine = Engine(
            sut=eval_expr,
            sqlite_conn=temp_conn,
            input_data=[sample_expression_1],
            sqlite_db=db_path,
            num_processes=1,
        )
        engine.execute([incorrect_relation_chain])
        conn = engine.results_to_duckdb()

    match conn.execute("SELECT * FROM input_data;").fetchall():
        case ((_, obj),):
            assert ast.unparse(pickle.loads(obj)) == ast.unparse(sample_expression_1)
        case _:
            raise ValueError(
                "Error extracting sample expression from returned duckdb connection."
            )

    assert [
        ("identity", 0),
        ("inverse", 1),
        ("subtract_1_from_expression", 2),
    ] == conn.execute(
        """
SELECT name, link_index
FROM applied_transformation
ORDER BY link_index;
                 """
    ).fetchall()

    assert [("equals",)] == conn.execute(
        "SELECT name FROM failed_invariant;"
    ).fetchall()
