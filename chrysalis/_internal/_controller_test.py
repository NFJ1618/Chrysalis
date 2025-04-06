from chrysalis._internal import _controller as controller


def test_register_string() -> None:
    controller.register("hello")
    controller.register("world")

    assert " ".join(controller._KNOWLEDGE_BASE) == "hello world"
