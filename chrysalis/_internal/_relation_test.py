import pytest

from chrysalis._internal._relation import KnowledgeBase


def test_create_relation() -> None:
    knowledge_base = KnowledgeBase[int, int]()
    with pytest.raises(
        ValueError,
        match="Registered transformation and invariant functions cannot be lambda functions.",
    ):
        knowledge_base.register(
            transformation=lambda x: x,
            invariant=lambda x, y: x == y,
        )
