from pathlib import Path

from chrysalis._internal import _tables as tables
from chrysalis._internal._relation import KnowledgeBase


def test_temporary_sqlite_db_deletes_success(
    mock_knowledge_base: KnowledgeBase,
) -> None:
    with tables.TemporarySqlite3RelationConnection(
        knowledge_base=mock_knowledge_base
    ) as (_, db_path):
        pass
    assert not db_path.exists()


def test_temporary_sqlite_db_deletes_error(mock_knowledge_base: KnowledgeBase) -> None:
    p: Path | None = None
    try:
        with tables.TemporarySqlite3RelationConnection(
            knowledge_base=mock_knowledge_base
        ) as (_, db_path):
            p = db_path
            raise RuntimeError(  # NOQA: TRY301
                "This runtime error is designed to ensure the sqlite database is deleted even if an error occurs during execution."
            )
    except Exception:  # NOQA: BLE001
        assert p is not None
        assert not p.exists()


def test_temporary_sqlite_db_fields(
    mock_knowledge_base: KnowledgeBase,
) -> None:
    with tables.TemporarySqlite3RelationConnection(
        knowledge_base=mock_knowledge_base
    ) as (conn, _):
        transformations_values = conn.execute(
            "SELECT name, id FROM transformation;"
        ).fetchall()
        invariants_values = conn.execute("SELECT name, id FROM invariant;").fetchall()

        assert {
            transformation_values[0] for transformation_values in transformations_values
        } == {
            "identity",
            "inverse",
            "add_1_to_expression",
            "subtract_1_from_expression",
        }
        assert {invariant_values[0] for invariant_values in invariants_values} == {
            "equals",
            "not_same_sign",
            "greater_than",
            "less_than",
        }
        assert conn.execute("SELECT COUNT(*) FROM relation;").fetchone()[0] == 5

        for transformation_name, transformation_id in transformations_values:
            assert transformation_name in mock_knowledge_base.transformation_ids
            assert (
                mock_knowledge_base.transformation_ids[transformation_name]
                == transformation_id
            )

            relation = mock_knowledge_base.relations[transformation_id]
            assert relation.transformation_name == transformation_name
            assert relation.transformation_id == transformation_id

            for invariant_id, invariant in relation.invariants.items():
                invariant_name = invariant.__name__
                assert invariant_name in mock_knowledge_base.invariant_ids
                assert mock_knowledge_base.invariant_ids[invariant_name] == invariant_id

        for invariant_name, invariant_id in invariants_values:
            assert invariant_name in mock_knowledge_base.invariant_ids
            assert mock_knowledge_base.invariant_ids[invariant_name] == invariant_id
