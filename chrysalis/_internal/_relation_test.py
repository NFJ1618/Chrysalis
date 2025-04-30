import ast

import pytest

from chrysalis._internal import _invariants as invariants
from chrysalis._internal._relation import KnowledgeBase
from chrysalis._internal.conftest import identity


def test_create_relation() -> None:
    knowledge_base = KnowledgeBase[ast.Expression, float]()
    knowledge_base.register(
        transformation=identity,
        invariant=invariants.equals,
    )

    assert len(knowledge_base.relations) == 1
    relation = next(iter(knowledge_base.relations.values()))
    assert relation.transformation_name == "identity"
    assert [invariant.__name__ for invariant in relation.invariants.values()] == [
        "equals"
    ]


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
