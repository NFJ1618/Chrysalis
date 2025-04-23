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

    relation = knowledge_base.relations[0]
    assert relation.transformation_name == "identity"
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
