from chrysalis._internal._relation import KnowledgeBase
from chrysalis._internal._search import SearchSpace


def test_metamorphic_search_random() -> None:
    knowledge_base = KnowledgeBase[int]()

    knowledge_base.register(
        name="identity",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )
    knowledge_base.register(
        name="inverse",
        transformation=lambda x: -1 * x,
        invariant=lambda x, y: x == -1 * y,
    )
    knowledge_base.register(
        name="double_negative",
        transformation=lambda x: -1 * 1 * x,
        invariant=lambda x, y: x == y,
    )

    search_space = SearchSpace(knowledge_base=knowledge_base)
    relation_chains = search_space.generate_chains(5)
    assert len(relation_chains) == 5
    assert all(len(relation_chain) == 10 for relation_chain in relation_chains)
    assert all(
        {relation.name for relation in relation_chain}.issubset(
            {"identity", "double_negative", "inverse"}
        )
        for relation_chain in relation_chains
    )
