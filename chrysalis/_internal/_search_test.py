from chrysalis._internal._relation import KnowledgeBase
from chrysalis._internal._search import SearchSpace


def identity(x: int) -> int:
    return x


def double_negative(x: int) -> int:
    return -1 * -1 * x


def inverse(x: int) -> int:
    return -1 * x


def equals(x: int, y: int) -> bool:
    return x == y


def not_equals(x: int, y: int) -> bool:
    return x != y


def test_metamorphic_search_random() -> None:
    knowledge_base = KnowledgeBase[int, int]()

    knowledge_base.register(
        transformation=identity,
        invariant=equals,
    )
    knowledge_base.register(
        transformation=inverse,
        invariant=not_equals,
    )
    knowledge_base.register(
        transformation=double_negative,
        invariant=equals,
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
