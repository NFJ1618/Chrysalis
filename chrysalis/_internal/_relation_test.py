import pytest

from chrysalis._internal._relation import KnowledgeBase


def identity(x: int) -> int:
    return x


def equals(x: int, y: int) -> bool:
    return x == y


def test_create_relation() -> None:
    knowledge_base = KnowledgeBase[int, int]()
    knowledge_base.register(
        transformation=identity,
        invariant=equals,
    )

    relation = knowledge_base.relations[0]
    assert relation.name == "identity"
    assert relation.invariants[0].__name__ == "equals"


def test_create_relation_lambda() -> None:
    knowledge_base = KnowledgeBase[int, int]()
    with pytest.raises(
        ValueError,
        match="Lambda functions cannot be used as transformation or invariants.",
    ):
        knowledge_base.register(
            transformation=lambda x: x,
            invariant=lambda x, y: x == y,
        )
