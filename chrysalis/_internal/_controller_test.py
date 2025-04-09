from chrysalis._internal import _controller as controller


def identity(x: int) -> int:
    return x


def inverse(x: int) -> int:
    return -1 * x


def equals(x: int, y: int) -> bool:
    return x == y


def not_equals(x: int, y: int) -> bool:
    return x != y


def is_same_sign(x: int, y: int) -> bool:
    return x >= 0 and y >= 0 or x <= 0 and y <= 0


def test_single_register() -> None:
    controller.new_knowledge_base()
    controller.register(
        transformation=identity,
        invariant=equals,
    )

    knowledge_base = controller._CURRENT_KNOWLEDGE_BASE

    assert knowledge_base is not None
    assert len(knowledge_base.relations) == 1
    assert knowledge_base.relations[0].name == "identity"


def test_multiple_register() -> None:
    controller.new_knowledge_base()
    controller.register(
        transformation=identity,
        invariant=equals,
    )
    controller.register(
        transformation=identity,
        invariant=is_same_sign,
    )
    controller.register(
        transformation=inverse,
        invariant=not_equals,
    )

    knowledge_base = controller._CURRENT_KNOWLEDGE_BASE

    assert knowledge_base is not None
    assert len(knowledge_base.relations) == 2
    assert {relation.name for relation in knowledge_base.relations} == {
        "identity",
        "inverse",
    }
    assert set(knowledge_base._relations["identity"].invariants) == {
        equals,
        is_same_sign,
    }
    assert knowledge_base._relations["inverse"].invariants == [not_equals]
