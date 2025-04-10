from collections import Counter

from chrysalis._internal._relation import KnowledgeBase


def test_create_relation() -> None:
    knowledge_base = KnowledgeBase[int]()
    knowledge_base.register(
        name="test_relation",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )

    relation = knowledge_base.relations[0]
    assert relation.name == "test_relation"
    assert knowledge_base._names == Counter({"test_relation": 1})


def test_create_multiple_relations() -> None:
    knowledge_base = KnowledgeBase[int]()
    knowledge_base.register(
        name="test_relation",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )

    knowledge_base.register(
        name="test_relation",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )

    knowledge_base.register(
        name="other_test_relation",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )

    assert {relation.name for relation in knowledge_base.relations} == {
        "test_relation",
        "test_relation_1",
        "other_test_relation",
    }
    assert knowledge_base._names == Counter(
        {"test_relation": 2, "other_test_relation": 1}
    )
