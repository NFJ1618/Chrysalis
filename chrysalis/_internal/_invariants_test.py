from chrysalis._internal import _invariants as invariants


def test_equals() -> None:
    assert invariants.equals(4, 4)
    assert not invariants.equals(3, 4)


def test_not_equals() -> None:
    assert not invariants.not_equals(4, 4)
    assert invariants.not_equals(3, 4)


def test_is_same_sign() -> None:
    assert invariants.is_same_sign(2, 2)
    assert invariants.is_same_sign(-2, -2)
    assert not invariants.is_same_sign(2, -2)

    assert invariants.is_same_sign(0, 2)
    assert invariants.is_same_sign(0, -2)
