import ast

from chrysalis._internal import _invariants as invariants
from chrysalis._internal._relation import KnowledgeBase
from chrysalis._internal._search import SearchSpace
from chrysalis._internal.conftest import (
    identity,
    inverse,
)


def test_metamorphic_search_random() -> None:
    knowledge_base = KnowledgeBase[ast.Expression, float]()

    knowledge_base.register(
        transformation=identity,
        invariant=invariants.equals,
    )
    knowledge_base.register(
        transformation=inverse,
        invariant=invariants.not_equals,
    )

    search_space = SearchSpace(knowledge_base=knowledge_base)
    relation_chains = search_space.generate_chains(5)
    assert len(relation_chains) == 5
    assert all(len(relation_chain) == 10 for relation_chain in relation_chains)
    assert all(
        {relation.transformation_name for relation in relation_chain}.issubset(
            {"identity", "inverse"}
        )
        for relation_chain in relation_chains
    )
