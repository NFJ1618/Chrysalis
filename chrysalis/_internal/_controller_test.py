from chrysalis._internal import _controller as controller


def test_single_register() -> None:
    controller.new_knowledge_base()
    controller.register(
        name="test_relation",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )

    knowledge_base = controller._CURRENT_KNOWLEDGE_BASE

    assert knowledge_base is not None
    assert len(knowledge_base.relations) == 1
    assert knowledge_base.relations[0].name == "test_relation"


def test_multiple_register() -> None:
    controller.new_knowledge_base()
    controller.register(
        name="test_relation_1",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )
    controller.register(
        name="test_relation_2",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )
    controller.register(
        name="test_relation_3",
        transformation=lambda x: x,
        invariant=lambda x, y: x == y,
    )

    knowledge_base = controller._CURRENT_KNOWLEDGE_BASE

    assert knowledge_base is not None
    print(knowledge_base)
    assert len(knowledge_base.relations) == 3
    assert {relation.name for relation in knowledge_base.relations} == {
        "test_relation_1",
        "test_relation_2",
        "test_relation_3",
    }
