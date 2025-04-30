import ast
import pickle

from chrysalis._internal._engine import Engine
from chrysalis._internal._relation import KnowledgeBase, Relation
from chrysalis._internal._tables import TemporarySqlite3RelationConnection
from chrysalis._internal.conftest import eval_expr


def test_successful_relation_chain(
    sample_expression_1: ast.Expression,
    correct_relation_chain: list[Relation[ast.Expression, float]],
    mock_knowledge_base: KnowledgeBase,
) -> None:
    with TemporarySqlite3RelationConnection(knowledge_base=mock_knowledge_base) as (
        temp_conn,
        db_path,
    ):
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
        ("add_1_to_expression", 2),
    ] == conn.execute(
        """
SELECT trans.name, appl_trans.link_index
FROM applied_transformation appl_trans
INNER JOIN transformation trans ON appl_trans.transformation = trans.id
ORDER BY appl_trans.link_index;
                 """
    ).fetchall()

    assert conn.execute("SELECT COUNT(*) FROM failed_invariant").fetchall() == [(0,)]


def test_unsuccessful_relation_chain(
    sample_expression_1: ast.Expression,
    incorrect_relation_chain: list[Relation[ast.Expression, float]],
    mock_knowledge_base: KnowledgeBase,
) -> None:
    with TemporarySqlite3RelationConnection(knowledge_base=mock_knowledge_base) as (
        temp_conn,
        db_path,
    ):
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
SELECT trans.name, appl_trans.link_index
FROM applied_transformation appl_trans
INNER JOIN transformation trans ON appl_trans.transformation = trans.id
ORDER BY appl_trans.link_index;
                 """
    ).fetchall()

    assert [("equals",)] == conn.execute(
        """
SELECT inv.name
FROM failed_invariant f_inv
INNER JOIN invariant inv ON f_inv.invariant = inv.id;
"""
    ).fetchall()
